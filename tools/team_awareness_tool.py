from tools.registry import registry, tool_result, tool_error
from pixel_state import SessionDB
import hashlib
import json
import time

def list_active_team(args: dict, **kwargs) -> str:
    """Return the list of hired active workers and their status."""
    db = SessionDB()
    session_id = kwargs.get("session_id")
    active_workers = [
        worker
        for worker in db.list_workers()
        if worker.status != "archived"
        and (not session_id or worker.manager_id == session_id)
    ]
    if not active_workers:
        return tool_result("No active workers in the team.")
        
    staff_info = "Current hired team members:\n"
    for w in active_workers:
        staff_info += f"- Worker ID: {w.worker_id} | Name: {w.display_name} | Role: {w.template_id} | Status: {w.status}\n"
    return tool_result(staff_info)

registry.register(
    name="list_active_team",
    description="Lists all currently hired workers in the team and their active status.",
    schema={
        "type": "object",
        "properties": {}
    },
    handler=list_active_team,
    toolset="delegation"
)

def propose_task_delegation(args: dict, **kwargs) -> str:
    """Delegate a task to an existing worker."""
    for nested_key in ("params", "arguments", "input", "data", "kwargs"):
        if isinstance(args.get(nested_key), dict):
            args = {**args, **args.get(nested_key)}

    worker_id = args.get("worker_id") or args.get("worker") or args.get("id")
    task_goal = args.get("goal") or args.get("task") or args.get("description") or args.get("instruction")
    deliverable = args.get("deliverable") or args.get("output") or args.get("expected_output") or args.get("result")
    acceptance_criteria = args.get("acceptance_criteria") or args.get("criteria") or args.get("acceptance")
    priority = args.get("priority", 0)
    
    if not worker_id or not task_goal or not deliverable or acceptance_criteria is None:
        return tool_error("worker_id, goal, deliverable, and acceptance_criteria are required")
        
    db = SessionDB()
    worker = db.get_worker(worker_id)
    if not worker:
        return tool_error(f"Worker {worker_id} not found.")
    if worker.status == 'archived':
        return tool_error(f"Worker {worker_id} is archived and cannot be assigned tasks.")

    if isinstance(acceptance_criteria, str):
        acceptance_criteria = [acceptance_criteria]

    if not isinstance(acceptance_criteria, list) or not acceptance_criteria:
        return tool_error("acceptance_criteria must be a non-empty list of verifiable conditions (or a string)")
    if not all(isinstance(item, str) and item.strip() for item in acceptance_criteria):
        return tool_error("Every acceptance_criteria item must be a non-empty string")
    try:
        priority = int(priority)
    except (TypeError, ValueError):
        return tool_error("priority must be an integer")

    session_id = kwargs.get("session_id", "agent")
    agent = kwargs.get("agent")
    
    # 1. Permission layer: Check delegates_to
    from pixel_cli.worker_registry import AgentRegistry
    caller_role = getattr(agent, "_delegate_role", None) if agent else None
    
    if caller_role:
        parent_template = AgentRegistry.get_template(caller_role)
        target_template = AgentRegistry.get_template(worker.template_id)
        if parent_template and parent_template.delegates_to:
            if target_template and target_template.id not in parent_template.delegates_to:
                return tool_error(f"Permission denied: Agent '{parent_template.name}' is not authorized to delegate to '{target_template.name}'. Allowed delegates: {parent_template.delegates_to}")
    
    if session_id and worker.manager_id != session_id:
        # If the caller role explicitly delegates to this template, we might allow cross-team, 
        # but for now respect the team boundary unless orchestrated otherwise.
        return tool_error(
            f"Worker {worker_id} does not belong to this team session. "
            "Use list_active_team to select one of this session's workers."
        )
    
    # 5. Canonical Task IDs: Use UUID instead of text hash
    import uuid
    task_id = f"task-{uuid.uuid4().hex}"
    
    now = time.time()
    
    def _create_task(conn):
        # 6. Worker Queue: Do NOT prevent queuing if worker is busy.
        # Manager can queue multiple tasks. WorkerSupervisor handles execution limit.
        conn.execute(
            "INSERT INTO delegate_tasks "
            "(id, parent_session_id, worker_role, worker_id, goal, deliverable, acceptance_criteria, priority, status, "
            "handoff_mode, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                task_id,
                session_id,
                worker.template_id,
                worker_id,
                task_goal,
                deliverable,
                json.dumps(acceptance_criteria),
                priority,
                "queued",
                "smart",
                now,
                now,
            ),
        )
        return {"created": True}

    try:
        outcome = db._execute_write(_create_task)
        
        # Ensure WorkerSupervisor is running
        try:
            from agent.worker_supervisor import ensure_worker_supervisor_started
            ensure_worker_supervisor_started()
        except Exception:
            pass
            
        return tool_result(f"Successfully delegated task to {worker_id}. Task ID: {task_id}")
    except Exception as e:
        return tool_error(f"Failed to delegate task: {e}")

registry.register(
    name="propose_task_delegation",
    description="Assign a subtask to an active team member (worker).",
    schema={
        "type": "object",
        "properties": {
            "worker_id": {
                "type": "string",
                "description": "The ID of the active worker to assign the task to."
            },
            "goal": {
                "type": "string",
                "description": "The specific task instructions for the worker. Must not be vague."
            },
            "deliverable": {
                "type": "string",
                "description": "What exactly the worker must produce (e.g., 'A React component file', 'A design review document')."
            },
            "acceptance_criteria": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "description": "Verifiable conditions that must be met for this task to be considered complete."
            },
            "priority": {
                "type": "integer",
                "description": "Priority of the task (higher is more important). Default 0."
            }
        },
        "required": ["worker_id", "goal", "deliverable", "acceptance_criteria"]
    },
    handler=propose_task_delegation,
    toolset="delegation"
)
