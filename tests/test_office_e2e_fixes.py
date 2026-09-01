import pytest
import time
import json
from pixel_state import SessionDB
from agent.worker_supervisor import WorkerSupervisor

@pytest.fixture
def fresh_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_state_fixes.db"
    monkeypatch.setattr("pixel_state.DEFAULT_DB_PATH", db_path)
    db = SessionDB()
    db.ensure_session("parent-123", source="test")
    return db

@pytest.mark.asyncio
async def test_worker_supervisor_dependency_validation(fresh_db, monkeypatch):
    db = fresh_db
    worker = db.hire_worker("dep-worker", "seo-specialist", "SEO Bob", "smart")
    db.update_worker("dep-worker", {"status": "idle"})
    now = time.time()
    
    # Insert a malformed dependency
    def _seed(conn):
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-malformed", "parent-123", "seo", "dep-worker", "Malformed", "queued", "smart", "{invalid-json}", now, now)
        )
        # Self dependency
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-self", "parent-123", "seo", "dep-worker", "Self", "queued", "smart", '["task-self"]', now, now)
        )
        # Missing dependency
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-missing", "parent-123", "seo", "dep-worker", "Missing", "queued", "smart", '["task-doesnotexist"]', now, now)
        )
        
    db._execute_write(_seed)
    supervisor = WorkerSupervisor(db=db)
    
    # Poll should immediately fail these tasks
    await supervisor._poll_queue()
    
    with db._read_ctx() as conn:
        statuses = {r["id"]: dict(r) for r in conn.execute("SELECT id, status, error_text FROM delegate_tasks").fetchall()}
        
    assert statuses["task-malformed"]["status"] == "error"
    assert "Malformed dependencies JSON" in statuses["task-malformed"]["error_text"]
    
    assert statuses["task-self"]["status"] == "error"
    assert "Self dependency detected" in statuses["task-self"]["error_text"]
    
    assert statuses["task-missing"]["status"] == "error"
    assert "Missing dependencies" in statuses["task-missing"]["error_text"]

