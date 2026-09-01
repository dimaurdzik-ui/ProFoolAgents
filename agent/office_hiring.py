"""Shared, durable hire-approval operations for every UI transport."""

from __future__ import annotations

import time
import uuid
from typing import Any

from agent.agent_registry import get_agent_template
from agent.office_events import enqueue_office_completion
from pixel_state import SessionDB


def approve_hire_request(task_id: str) -> dict[str, Any]:
    """Atomically hire the requested worker; never auto-assign a task."""
    if not isinstance(task_id, str) or not task_id:
        return {"success": False, "error": "task_id is required"}

    db = SessionDB()
    now = time.time()

    def _approve(conn):
        row = conn.execute(
            "SELECT pending_hire_template_id, parent_session_id, handoff_mode, status "
            "FROM delegate_tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
        if not row:
            return {"error": f"Task {task_id} not found in SessionDB"}
        if row["status"] != "waiting_hire_approval":
            return {"error": f"Hire request {task_id} is already {row['status']}."}
        template_id = row["pending_hire_template_id"]
        template = get_agent_template(template_id) if template_id else None
        if not template:
            return {"error": f"Worker template '{template_id}' no longer exists."}
        autonomy_mode = row["handoff_mode"]
        if autonomy_mode not in {"manual", "smart", "autonomous"}:
            autonomy_mode = "smart"
        worker_id = f"{template_id}-{uuid.uuid4().hex[:8]}"
        conn.execute(
            "INSERT INTO workers (worker_id, template_id, display_name, autonomy_mode, status, manager_id, created_at) "
            "VALUES (?, ?, ?, ?, 'idle', ?, ?)",
            (worker_id, template_id, template.name, autonomy_mode, row["parent_session_id"], now),
        )
        conn.execute(
            "UPDATE delegate_tasks SET status = 'completed', updated_at = ? WHERE id = ?",
            (now, task_id),
        )
        return {
            "worker_id": worker_id,
            "template_id": template_id,
            "parent_session_id": row["parent_session_id"],
        }

    approved = db._execute_write(_approve)
    if "error" in approved:
        return {"success": False, "error": approved["error"]}
    enqueue_office_completion(
        db,
        parent_session_id=approved["parent_session_id"],
        task_id=task_id,
        worker_id=approved["worker_id"],
        goal=f"Hire {approved['template_id']}",
        summary=(
            f"Hire approved: {approved['worker_id']} is now available. "
            "Delegate a task explicitly if work is needed."
        ),
    )
    return {"success": True, "worker_id": approved["worker_id"]}


def reject_hire_request(task_id: str) -> dict[str, Any]:
    """Reject one pending hire request exactly once."""
    if not isinstance(task_id, str) or not task_id:
        return {"success": False, "error": "task_id is required"}

    db = SessionDB()
    now = time.time()

    def _reject(conn):
        row = conn.execute(
            "SELECT parent_session_id, status FROM delegate_tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if not row:
            return {"error": f"Task {task_id} not found in SessionDB"}
        if row["status"] != "waiting_hire_approval":
            return {"error": f"Hire request {task_id} is already {row['status']}."}
        conn.execute(
            "UPDATE delegate_tasks SET status = 'rejected', updated_at = ? WHERE id = ?",
            (now, task_id),
        )
        return {"parent_session_id": row["parent_session_id"]}

    rejected = db._execute_write(_reject)
    if "error" in rejected:
        return {"success": False, "error": rejected["error"]}
    enqueue_office_completion(
        db,
        parent_session_id=rejected["parent_session_id"],
        task_id=task_id,
        goal="Hire request",
        status="failed",
        error="The user rejected the hire proposal.",
    )
    return {"success": True}
