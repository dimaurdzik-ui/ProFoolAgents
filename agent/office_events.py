"""Delivery adapter for durable Office task state changes.

Office workers persist their task outcome in ``SessionDB`` first.  This module
then uses the existing process-notification rail to wake the parent session;
it deliberately does not invent a second, gateway-only completion queue.
"""

from __future__ import annotations

from typing import Any


def enqueue_office_completion(
    session_db: Any,
    *,
    parent_session_id: str | None,
    task_id: str,
    worker_id: str | None = None,
    goal: str = "",
    status: str = "completed",
    summary: str = "",
    error: str = "",
) -> bool:
    """Queue a parent-session notification after its durable state is written.

    The process registry is already drained by both the CLI and gateway.  The
    task/attempt rows remain the source of truth if a notification is missed.
    """
    if not parent_session_id or parent_session_id == "agent":
        return False

    parent = session_db.get_session(parent_session_id)
    if not parent:
        return False

    from tools.process_registry import process_registry

    process_registry.completion_queue.put(
        {
            "type": "async_delegation",
            "session_key": parent.get("session_key") or parent_session_id,
            "origin_session_id": parent_session_id,
            "parent_session_id": parent_session_id,
            "goal": goal or f"Office task {task_id}",
            "role": "office_worker",
            "model": "",
            "status": "error" if status in {"failed", "error"} else "completed",
            "summary": summary,
            "error": error,
            "api_calls": 0,
            "duration_seconds": 0,
            "office_task_id": task_id,
            "worker_id": worker_id or "",
        }
    )
    return True
