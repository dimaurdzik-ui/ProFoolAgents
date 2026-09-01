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


@pytest.mark.asyncio
async def test_dependency_cycles(fresh_db, monkeypatch):
    db = fresh_db
    worker = db.hire_worker("cycle-worker", "seo-specialist", "SEO Bob", "smart")
    db.update_worker("cycle-worker", {"status": "idle"})
    now = time.time()
    
    def _seed(conn):
        # A -> B -> A cycle
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-A1", "parent-123", "seo", "cycle-worker", "A1", "queued", "smart", '["task-B1"]', now, now)
        )
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-B1", "parent-123", "seo", "cycle-worker", "B1", "queued", "smart", '["task-A1"]', now, now)
        )
        
        # A -> B -> C -> A cycle
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-A2", "parent-123", "seo", "cycle-worker", "A2", "queued", "smart", '["task-B2"]', now, now)
        )
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-B2", "parent-123", "seo", "cycle-worker", "B2", "queued", "smart", '["task-C2"]', now, now)
        )
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, dependencies_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-C2", "parent-123", "seo", "cycle-worker", "C2", "queued", "smart", '["task-A2"]', now, now)
        )
        
    db._execute_write(_seed)
    supervisor = WorkerSupervisor(db=db)
    
    await supervisor._poll_queue()
    
    with db._read_ctx() as conn:
        statuses = {r["id"]: dict(r) for r in conn.execute("SELECT id, status, error_text FROM delegate_tasks").fetchall()}
        
    for task_id in ["task-A1", "task-B1", "task-A2", "task-B2", "task-C2"]:
        assert statuses[task_id]["status"] == "error"
        assert "Cyclic dependency" in statuses[task_id]["error_text"] or "Dependency failed" in statuses[task_id]["error_text"]

@pytest.mark.asyncio
async def test_delegates_to_professional_agent(fresh_db, monkeypatch):
    """Test that professional agent_id correctly applies delegates_to and nameless caller gets denied."""
    from agent.agent_registry import AgentRegistry, AgentTemplate
    registry = AgentRegistry.get_instance()
    
    # Setup test templates
    t_manager = AgentTemplate(id="test-manager", name="Test Manager", category="test", description="", prompt_version=1, allowed_tools=[], starter_prompts=[], capabilities=[], system_prompt="", delegates_to=["test-worker"])
    t_worker = AgentTemplate(id="test-worker", name="Test Worker", category="test", description="", prompt_version=1, allowed_tools=[], starter_prompts=[], capabilities=[], system_prompt="", delegates_to=[])
    
    registry._templates["test-manager"] = t_manager
    registry._templates["test-worker"] = t_worker

    # Mock agent with professional identity
    class MockAgent:
        def __init__(self, agent_id=None, office_id=None):
            self.agent_id = agent_id
            self._session_init_model_config = {"_office_template_id": office_id} if office_id else {}

    manager_agent = MockAgent(agent_id="test-manager")
    worker_agent = MockAgent(agent_id="test-worker")
    unknown_agent = MockAgent()
    
    from tools.team_awareness_tool import propose_task_delegation
    from tools.delegate_tool import delegate_task
    
    worker = fresh_db.hire_worker("test-worker", "test-worker", "Test Worker", "smart")
    fresh_db.update_worker("test-worker", {"status": "idle", "manager_id": "parent-123"})
    manager = fresh_db.hire_worker("test-manager", "test-manager", "Test Manager", "smart")
    fresh_db.update_worker("test-manager", {"status": "idle", "manager_id": "parent-123"})
    
    # propose_task_delegation tests
    res = propose_task_delegation({"worker_id": "test-worker", "goal": "do it", "deliverable": "done", "priority": 1, "acceptance_criteria": ["done"]}, agent=manager_agent, session_id="parent-123")
    assert "Successfully" in res, f"Manager should delegate to worker: {res}"
    
    res = propose_task_delegation({"worker_id": "test-manager", "goal": "do it", "deliverable": "done", "priority": 1, "acceptance_criteria": ["done"]}, agent=worker_agent, session_id="parent-123")
    assert "error" in res and "not authorized" in res, f"Worker should NOT delegate to manager: {res}"
    
    res = propose_task_delegation({"worker_id": "test-worker", "goal": "do it", "deliverable": "done", "priority": 1, "acceptance_criteria": ["done"]}, agent=unknown_agent, session_id="parent-123")
    assert "error" in res and "could not be determined" in res, f"Unknown agent should NOT delegate: {res}"
    
@pytest.mark.asyncio
async def test_messenger_task_permissions(fresh_db, monkeypatch):
    """Test task-scoped messaging permissions and team-scoped non-task permissions."""
    db = fresh_db
    now = time.time()
    
    db.hire_worker("worker-assignee", "test", "A", "smart")
    db.hire_worker("worker-colleague", "test", "B", "smart")
    db.hire_worker("worker-other", "test", "C", "smart")
    
    db.update_worker("worker-assignee", {"manager_id": "team-1", "status": "idle"})
    db.update_worker("worker-colleague", {"manager_id": "team-1", "status": "idle"})
    db.update_worker("worker-other", {"manager_id": "team-2", "status": "idle"})
    
    def _seed(conn):
        conn.execute(
            "INSERT INTO sessions (id, source, started_at) VALUES (?, ?, ?)",
            ("manager-1", "test", now)
        )
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-123", "manager-1", "test", "worker-assignee", "goal", "working", "smart", now, now)
        )
    db._execute_write(_seed)
    
    monkeypatch.setattr("pixel_state.SessionDB", lambda: fresh_db)
    from tools.send_message_tool import _deliver_worker_message
    
    # 1. Unrelated same-team worker CANNOT write to another's task
    res = json.loads(_deliver_worker_message("worker-assignee", "msg", sender_id="worker-colleague", task_id="task-123"))
    assert "error" in res and "Permission denied" in res["error"]
    
    # 2. Manager CAN write to task
    res = json.loads(_deliver_worker_message("worker-assignee", "msg", sender_id="manager-1", task_id="task-123"))
    assert res.get("success") is True
    
    # 3. Normal same-team chat without task_id WORKS
    res = json.loads(_deliver_worker_message("worker-assignee", "msg", sender_id="worker-colleague"))
    assert res.get("success") is True
    
    # 4. Cross-team chat without task_id FAILS
    res = json.loads(_deliver_worker_message("worker-assignee", "msg", sender_id="worker-other"))
    assert "error" in res and "Permission denied" in res["error"]


