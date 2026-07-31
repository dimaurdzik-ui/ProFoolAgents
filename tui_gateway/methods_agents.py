from tui_gateway.method_ctx import HandlerRegistry

_registry = HandlerRegistry()
method = _registry.method

@method("agents.catalog")
def _(rid, params: dict) -> dict:
    import dataclasses

    from agent.agent_registry import TEAM_AGENT_ID, get_all_agent_templates

    catalog = [template for template in get_all_agent_templates() if template.id != TEAM_AGENT_ID]
    return _ok(rid, {"catalog": [dataclasses.asdict(t) for t in catalog]})

@method("agents.installed")
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB

    db = SessionDB()
    installed = db.list_installed_agents()
    return _ok(rid, {"installed": installed})

@method("agents.install")
def _(rid, params: dict) -> dict:
    import re

    from agent.agent_registry import get_agent_template
    from pixel_state import SessionDB

    agent_id = params.get("agent_id")
    if not isinstance(agent_id, str) or re.fullmatch(r"[a-zA-Z0-9_-]+", agent_id) is None:
        return _err(rid, 400, "Invalid or missing agent_id")
        
    template = get_agent_template(agent_id)
    if not template or not template.enabled:
        return _err(rid, 404, "Agent template not found or disabled")
        
    db = SessionDB()
    try:
        db.install_agent(agent_id, template.id, template.prompt_version)
        return _ok(rid, {"success": True})
    except Exception as e:
        return _err(rid, 500, str(e))

@method("agents.uninstall")
def _(rid, params: dict) -> dict:
    import re

    from pixel_state import SessionDB

    agent_id = params.get("agent_id")
    if not isinstance(agent_id, str) or re.fullmatch(r"[a-zA-Z0-9_-]+", agent_id) is None:
        return _err(rid, 400, "Invalid or missing agent_id")
    db = SessionDB()
    try:
        db.uninstall_agent(agent_id)
        return _ok(rid, {"success": True})
    except Exception as e:
        return _err(rid, 500, str(e))

@method("session.set_agent")
def _(rid, params: dict) -> dict:
    import re

    from agent.agent_registry import get_agent_template
    from pixel_state import SessionDB

    session_id = params.get("session_id")
    agent_id = params.get("agent_id")
    if not session_id:
        return _err(rid, 400, "session_id is required")
    
    db = SessionDB()
    live_session = None
    live_id = None
    with _sessions_lock:
        for candidate_id, candidate in _sessions.items():
            if candidate_id == session_id or candidate.get("session_key") == session_id:
                live_id, live_session = candidate_id, candidate
                break
    session = db.get_session(session_id)
    if not session and live_session is None:
        return _err(rid, 404, "session not found")
        
    try:
        if agent_id:
            if not isinstance(agent_id, str) or re.fullmatch(r"[a-zA-Z0-9_-]+", agent_id) is None:
                return _err(rid, 400, "Invalid agent_id")
            
            template = get_agent_template(agent_id)
            if not template or not template.enabled:
                return _err(rid, 404, "Agent template not found or disabled")
            
            installed = [a["id"] for a in db.list_installed_agents()]
            if agent_id not in installed:
                return _err(rid, 403, "Agent is not installed")
                
            prompt_version = template.prompt_version
        else:
            prompt_version = None

        # Draft sessions deliberately do not exist in SQLite until their first
        # prompt. Keep the chosen identity on the live record now; the normal
        # first-turn persistence path writes it atomically with the session.
        if live_session is not None:
            if live_session.get("running"):
                return _err(rid, 409, "Cannot change an agent while it is running")
            live_session["agent_id"] = agent_id or None
            live_session["agent_prompt_version"] = prompt_version
        if session:
            db.update_session_agent(session_id, agent_id or None, prompt_version)
        return _ok(rid, {"success": True, "agent_id": agent_id or None, "prompt_version": prompt_version})
    except Exception as e:
        return _err(rid, 500, str(e))

@method("session.agent")
def _(rid, params: dict) -> dict:
    from pixel_state import SessionDB

    session_id = params.get("session_id")
    if not session_id:
        return _err(rid, 400, "session_id is required")

    with _sessions_lock:
        for candidate_id, candidate in _sessions.items():
            if candidate_id == session_id or candidate.get("session_key") == session_id:
                # Newly created drafts own this value in memory. Resumed
                # sessions predate the field, so fall through to SQLite rather
                # than incorrectly presenting them as the general chat.
                if "agent_id" in candidate:
                    return _ok(rid, {"agent_id": candidate.get("agent_id")})
                break

    session = SessionDB().get_session(session_id)
    if not session:
        return _err(rid, 404, "session not found")
    return _ok(rid, {"agent_id": session.get("agent_id")})

def register(server) -> None:
    _registry.install(server)
