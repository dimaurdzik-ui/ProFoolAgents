from tui_gateway.method_ctx import HandlerRegistry

_registry = HandlerRegistry()
method = _registry.method
_profile_scoped = _registry.profile_scoped

@method("workers.hire")
@_profile_scoped
def _(rid, params: dict) -> dict:
    import re

    from pixel_state import SessionDB
    from agent.agent_registry import get_agent_template

    worker_id = params.get("worker_id")
    template_id = params.get("template_id")
    display_name = params.get("display_name")
    autonomy_mode = params.get("autonomy_mode", "smart")
    manager_id = params.get("manager_id")

    if not isinstance(worker_id, str) or re.fullmatch(r"[a-zA-Z0-9_-]+", worker_id) is None:
        return _err(rid, 400, "Invalid or missing worker_id")
    if not isinstance(template_id, str):
        return _err(rid, 400, "Invalid or missing template_id")
    if autonomy_mode not in {"manual", "smart", "autonomous"}:
        return _err(rid, 400, "autonomy_mode must be manual, smart, or autonomous")

    template = get_agent_template(template_id)
    if not template or not template.enabled:
        return _err(rid, 404, "Agent template not found or disabled")

    db = SessionDB()
    try:
        if db.get_worker(worker_id):
            return _err(rid, 409, "Worker already exists")
        if manager_id and not db.get_worker(manager_id):
            return _err(rid, 404, "Manager worker not found")

        worker = db.hire_worker(worker_id, template_id, display_name or template.name, autonomy_mode, manager_id)
        db.update_worker(worker_id, {"status": "idle"})
        worker = db.get_worker(worker_id)

        from agent.worker_supervisor import ensure_worker_supervisor_started
        ensure_worker_supervisor_started()
        return _ok(rid, {"worker": worker.__dict__})
    except Exception as e:
        return _err(rid, 500, str(e))

@method("workers.update")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB

    worker_id = params.get("worker_id")
    if not worker_id:
        return _err(rid, 400, "worker_id is required")

    updates = params.get("updates", {})
    if not isinstance(updates, dict) or not updates:
        return _err(rid, 400, "updates are required")
    unknown = set(updates) - {"display_name", "status", "autonomy_mode", "manager_id"}
    if unknown:
        return _err(rid, 400, f"Unsupported worker fields: {', '.join(sorted(unknown))}")
    if "status" in updates and updates["status"] not in {"onboarding", "idle", "paused", "error"}:
        return _err(rid, 400, "status must be onboarding, idle, paused, or error")
    if "autonomy_mode" in updates and updates["autonomy_mode"] not in {"manual", "smart", "autonomous"}:
        return _err(rid, 400, "autonomy_mode must be manual, smart, or autonomous")

    db = SessionDB()
    try:
        worker = db.get_worker(worker_id)
        if not worker:
            return _err(rid, 404, "Worker not found")
        manager_id = updates.get("manager_id")
        if manager_id == worker_id:
            return _err(rid, 400, "A worker cannot manage itself")
        if manager_id and not db.get_worker(manager_id):
            return _err(rid, 404, "Manager worker not found")

        success = db.update_worker(worker_id, updates)
        if success:
            worker = db.get_worker(worker_id)
            return _ok(rid, {"worker": worker.__dict__})
        return _err(rid, 400, "Failed to update worker or no valid fields provided")
    except Exception as e:
        return _err(rid, 500, str(e))

@method("workers.archive")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB

    worker_id = params.get("worker_id")
    if not worker_id:
        return _err(rid, 400, "worker_id is required")

    db = SessionDB()
    try:
        worker = db.get_worker(worker_id)
        if not worker:
            return _err(rid, 404, "Worker not found")

        if db.archive_worker(worker_id):
            return _ok(rid, {"success": True})
        return _err(rid, 404, "Worker not found")
    except Exception as e:
        return _err(rid, 500, str(e))

@method("workers.list")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB

    include_archived = params.get("include_archived", False)
    db = SessionDB()
    try:
        workers = db.list_workers(include_archived=include_archived)
        return _ok(rid, {"workers": [w.__dict__ for w in workers]})
    except Exception as e:
        return _err(rid, 500, str(e))


@method("tasks.approve_hire")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from agent.office_hiring import approve_hire_request

    result = approve_hire_request(params.get("task_id"))
    if not result.get("success"):
        return _err(rid, 409, result.get("error", "Could not approve hire"))
    return _ok(rid, result)


@method("tasks.reject_hire")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from agent.office_hiring import reject_hire_request

    result = reject_hire_request(params.get("task_id"))
    if not result.get("success"):
        return _err(rid, 409, result.get("error", "Could not reject hire"))
    return _ok(rid, result)

@method("tasks.approve")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB
    import time

    task_id = params.get("task_id")
    if not task_id:
        return _err(rid, 400, "task_id is required")

    db = SessionDB()
    now = time.time()
    try:
        def _approve(conn):
            cursor = conn.execute(
                "UPDATE delegate_tasks SET status = 'completed', updated_at = ? "
                "WHERE id = ? AND status = 'waiting_approval'",
                (now, task_id),
            )
            if cursor.rowcount == 0:
                return False
            conn.execute(
                "UPDATE delegate_task_attempts SET status = 'completed' "
                "WHERE id = (SELECT id FROM delegate_task_attempts "
                "WHERE task_id = ? AND status = 'waiting_approval' "
                "ORDER BY attempt_number DESC LIMIT 1)",
                (task_id,),
            )
            return True

        if not db._execute_write(_approve):
            return _err(rid, 409, "Task is not waiting for approval")
        return _ok(rid, {"success": True})
    except Exception as e:
        return _err(rid, 500, str(e))

@method("tasks.reject")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB
    import time

    task_id = params.get("task_id")
    feedback = params.get("feedback")

    if not task_id or not feedback:
        return _err(rid, 400, "task_id and feedback are required")

    db = SessionDB()
    now = time.time()
    try:
        def _reject(conn):
            cursor = conn.execute(
                "UPDATE delegate_tasks SET status = 'queued', updated_at = ? "
                "WHERE id = ? AND status = 'waiting_approval'",
                (now, task_id),
            )
            if cursor.rowcount == 0:
                return False
            conn.execute(
                "UPDATE delegate_task_attempts SET status = 'rejected', review_feedback = ? "
                "WHERE id = (SELECT id FROM delegate_task_attempts "
                "WHERE task_id = ? AND status = 'waiting_approval' "
                "ORDER BY attempt_number DESC LIMIT 1)",
                (feedback, task_id),
            )
            return True

        if not db._execute_write(_reject):
            return _err(rid, 409, "Task is not waiting for approval")
        return _ok(rid, {"success": True})
    except Exception as e:
        return _err(rid, 500, str(e))


@method("tasks.list")
@_profile_scoped
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB

    status = params.get("status")
    if status is not None and status not in {
        "queued", "working", "waiting_approval", "completed", "error"
    }:
        return _err(rid, 400, "Invalid task status")
    db = SessionDB()
    try:
        sql = (
            "SELECT t.*, w.display_name AS worker_name, "
            "a.result AS result, a.review_feedback AS review_feedback, "
            "a.attempt_number AS attempt_number, "
            "a.child_session_id AS child_session_id, "
            "s.model AS execution_model, "
            "s.billing_provider AS execution_provider, "
            "s.billing_base_url AS execution_base_url "
            "FROM delegate_tasks t "
            "LEFT JOIN workers w ON w.worker_id = t.worker_id "
            "LEFT JOIN delegate_task_attempts a ON a.id = ("
            "SELECT latest.id FROM delegate_task_attempts latest "
            "WHERE latest.task_id = t.id "
            "ORDER BY latest.attempt_number DESC LIMIT 1) "
            "LEFT JOIN sessions s ON s.id = a.child_session_id"
        )
        values = ()
        if status:
            sql += " WHERE t.status = ?"
            values = (status,)
        sql += " ORDER BY t.created_at DESC LIMIT 200"
        with db._read_ctx() as conn:
            rows = [dict(row) for row in conn.execute(sql, values).fetchall()]
        return _ok(rid, {"tasks": rows})
    except Exception as e:
        return _err(rid, 500, str(e))

def register(server) -> None:
    _registry.install(server)
