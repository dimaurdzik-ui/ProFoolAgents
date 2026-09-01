"""
propose_hire_tool — Agent tool to propose hiring a new specialist.

IMPORTANT: This tool writes to SessionDB (state.db) which is the SAME storage
that WorkerSupervisor reads from. Previously it wrote to workers.db (pixel_cli.worker_db)
which WorkerSupervisor never observed — creating a dead loop.

Flow:
  1. Agent calls propose_hire_worker(template_id, reason, suggested_task)
  2. Tool inserts a waiting hire request into SessionDB
  3. The user approves or rejects it in Desktop
  4. On approval, the orchestrator explicitly delegates work if needed.
"""

import time
import uuid
import logging

from tools.registry import registry, tool_result, tool_error
from pixel_state import SessionDB

logger = logging.getLogger(__name__)


def propose_hire_worker(args: dict, **kwargs) -> str:
    """Propose hiring a worker; approval does not assign work automatically."""
    if isinstance(args, str):
        import json
        try:
            args = json.loads(args)
        except Exception:
            args = {"reason": args}
    elif not isinstance(args, dict):
        args = {}

    # Unpack nested structures if present
    for nested_key in ("params", "arguments", "input", "data", "kwargs"):
        if isinstance(args.get(nested_key), dict):
            args = {**args, **args.get(nested_key)}

    template_id = (
        args.get("template_id")
        or args.get("role")
        or args.get("template")
        or args.get("worker_role")
        or args.get("worker")
        or args.get("specialist")
        or args.get("name")
        or args.get("role_id")
        or args.get("worker_type")
    )
    if not isinstance(template_id, str) or not template_id.strip():
        return tool_error(
            "Missing required 'template_id'. Specify the specialist to hire "
            "(for example: 'ui-designer' or 'seo-specialist')."
        )
    template_id = template_id.strip()

    reason = (
        args.get("reason")
        or args.get("description")
        or args.get("goal")
        or args.get("suggested_task")
        or args.get("task")
        or args.get("purpose")
        or args.get("message")
        or args.get("prompt")
    )
    if not isinstance(reason, str) or not reason.strip():
        return tool_error(
            "Missing required 'reason' or 'suggested_task'. Describe why the "
            f"'{template_id}' specialist is needed."
        )
    reason = reason.strip()

    suggested_task = args.get("suggested_task") or args.get("task") or reason
    if not isinstance(suggested_task, str) or not suggested_task.strip():
        return tool_error(
            "'suggested_task' must be a non-empty, concrete task description. "
            "Example: 'Build a landing page with hero section, features, and CTA using React and Tailwind.'"
        )
    suggested_task = suggested_task.strip()

    # Reject vague/placeholder goals that give the worker no real context.
    # A quality task must:
    #   - be at least 40 characters long
    #   - not be a generic placeholder phrase
    _VAGUE_PATTERNS = (
        "assist the team",
        "help the team",
        "work as a",
        "act as a",
        "be a ",
        "support the team",
        "help with tasks",
        "assist with tasks",
    )
    _task_lower = suggested_task.lower()
    if len(suggested_task) < 40:
        return tool_error(
            f"'suggested_task' is too vague ({len(suggested_task)} chars). "
            "Provide a concrete, specific task description of at least 40 characters. "
            "Include: what to build/do, the technology stack, and expected outputs. "
            f"Example: 'Create a responsive landing page for an AI services company with "
            f"hero, features, testimonials, FAQ, and CTA sections in plain HTML/CSS/JS.'"
        )
    if any(_task_lower.startswith(p) for p in _VAGUE_PATTERNS):
        return tool_error(
            f"'suggested_task' looks like a placeholder: '{suggested_task}'. "
            "Provide a concrete task with specific deliverables rather than a generic role description."
        )
    autonomy_mode = args.get("autonomy_mode", "smart")

    task_id = kwargs.get("task_id")
    session_id = kwargs.get("session_id", "")

    # Verify the template exists before creating the worker
    try:
        from agent.agent_registry import get_agent_template
        template = get_agent_template(template_id)
        if not template:
            return tool_error(
                f"Template '{template_id}' not found in config/agents/. "
                f"Available templates: developer, ui-designer, backend-developer, "
                f"data-analyst, seo-specialist, project-manager, etc."
            )
    except Exception as e:
        logger.warning("Could not verify template '%s': %s", template_id, e)
        # Continue anyway — supervisor will catch it at runtime

    db = SessionDB()

    # Ensure parent session exists
    if session_id:
        try:
            db.ensure_session(session_id, source="agent")
        except Exception:
            pass

    # Generate IDs
    delegate_task_id = f"task-{uuid.uuid4().hex[:8]}"
    display_name = template_id.replace("-", " ").title() if template else template_id

    try:
        now = time.time()
        def _create_hire_request(conn):
            conn.execute(
                "INSERT INTO delegate_tasks "
                "(id, parent_session_id, worker_role, goal, status, "
                "handoff_mode, created_at, updated_at, "
                "pending_hire_template_id, pending_hire_reason, pending_hire_task) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    delegate_task_id,
                    session_id or "agent",
                    "hire_request",
                    f"Hire {template_id}: {reason[:50]}...",
                    "waiting_hire_approval",
                    autonomy_mode,
                    now,
                    now,
                    template_id,
                    reason,
                    suggested_task,
                ),
            )

        db._execute_write(_create_hire_request)
        logger.info(
            "propose_hire_worker: created hire request %s for template %s",
            delegate_task_id, template_id
        )
    except Exception as e:
        return tool_error(f"Failed to create hire request for '{template_id}': {e}")

    return tool_result(
        f"A request to hire '{display_name}' ({template_id}) has been submitted.\n"
        f"Task ID: {delegate_task_id}\n"
        f"Goal: {suggested_task}\n\n"
        f"The user must approve this hire in the Desktop app before the worker is created. "
        f"After approval, delegate work explicitly using the returned worker ID."
    )


registry.register(
    name="propose_hire_worker",
    description=(
        "Propose hiring a new specialist worker for the team. The worker is created "
        "only after user approval; delegate work separately with propose_task_delegation. "
        "Use this when a task requires a specialist role that would run in parallel "
        "or independently from your current work."
    ),
    schema={
        "type": "object",
        "properties": {
            "template_id": {
                "type": "string",
                "description": (
                    "Role template to hire. Available: developer, ui-designer, "
                    "backend-developer, frontend-developer, data-analyst, seo-specialist, "
                    "project-manager, operations-manager, content-marketer, "
                    "social-media-manager, ux-designer, ux-researcher, devops-engineer, "
                    "database-engineer, ai-engineer, financial-analyst, brand-strategist."
                ),
            },
            "reason": {
                "type": "string",
                "description": "Why this specialist is needed for the current project.",
            },
            "suggested_task": {
                "type": "string",
                "description": (
                    "Concrete, specific task to assign upon hiring. Must be at least 40 characters "
                    "and describe exactly what to build or do, which technologies to use, and the "
                    "expected deliverable. BAD: 'Assist the team as a developer'. "
                    "GOOD: 'Build a responsive single-page landing for an AI SaaS company with "
                    "hero section, feature grid, pricing table, FAQ accordion, and contact form "
                    "using vanilla HTML/CSS/JS with smooth scroll animations.'"
                ),
            },
            "autonomy_mode": {
                "type": "string",
                "enum": ["manual", "smart", "autonomous"],
                "description": (
                    "'autonomous' = worker completes and marks done automatically. "
                    "'smart' (default) = worker completes but waits for user approval. "
                    "'manual' = worker asks approval before each tool call."
                ),
            },
        },
        "required": ["template_id", "reason", "suggested_task"],
    },
    handler=propose_hire_worker,
    toolset="delegation",
)
