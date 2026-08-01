import asyncio
import time
from pathlib import Path

import pytest

from agent.worker_supervisor import WorkerSupervisor
from pixel_state import SessionDB


@pytest.fixture
def fresh_db(tmp_path, monkeypatch):
    # Monkeypatch the DB path to a temporary file
    db_path = tmp_path / "test_state.db"
    monkeypatch.setattr("pixel_state.DEFAULT_DB_PATH", db_path)
    # SessionDB must create the production schema; the test must not maintain
    # a permissive shadow copy of it.
    db = SessionDB()
    db.ensure_session("parent-123", source="test")
    return db


def test_team_cli_uses_session_db_and_archives_worker(fresh_db, capsys):
    from cli import PixelAgentsCLI

    db = fresh_db
    db.hire_worker("cli-worker", "seo-specialist", "CLI SEO")
    db.update_worker("cli-worker", {"status": "idle"})
    shell = PixelAgentsCLI.__new__(PixelAgentsCLI)
    shell._session_db = db

    shell._handle_team("/team list")
    assert "CLI SEO" in capsys.readouterr().out
    shell._handle_team("/team archive cli-worker")
    assert "Archived worker cli-worker" in capsys.readouterr().out
    assert db.get_worker("cli-worker").status == "archived"
    db.close()


def test_cron_enqueues_worker_task_with_valid_parent_session(fresh_db, monkeypatch):
    from cron.scheduler import run_job

    db = fresh_db
    db.hire_worker("cron-worker", "seo-specialist", "Cron SEO", "autonomous")
    db.update_worker("cron-worker", {"status": "idle"})
    monkeypatch.setattr(
        "agent.worker_supervisor.ensure_worker_supervisor_started",
        lambda: None,
    )

    success, _, final_response, error = run_job({
        "id": "office-cron",
        "name": "Office cron",
        "prompt": "Daily audit",
        "worker_id": "cron-worker",
    })
    assert success is True
    assert final_response == "SILENT_MARKER"
    assert error is None
    with db._read_ctx() as conn:
        task = conn.execute(
            "SELECT parent_session_id, worker_id, status, handoff_mode FROM delegate_tasks"
        ).fetchone()
        parent_exists = conn.execute(
            "SELECT 1 FROM sessions WHERE id = ?", (task["parent_session_id"],)
        ).fetchone()
    assert dict(task) == {
        "parent_session_id": "cron_office-cron",
        "worker_id": "cron-worker",
        "status": "queued",
        "handoff_mode": "autonomous",
    }
    assert parent_exists is not None
    db.close()


def test_worker_rpc_contract_for_desktop_and_tui(fresh_db, monkeypatch):
    from tui_gateway import server

    monkeypatch.setattr(
        "agent.worker_supervisor.ensure_worker_supervisor_started",
        lambda: None,
    )

    hired = server._methods["workers.hire"](
        1,
        {
            "autonomy_mode": "smart",
            "display_name": "Office SEO",
            "template_id": "seo-specialist",
            "worker_id": "office-seo",
        },
    )
    assert hired["result"]["worker"]["status"] == "idle"

    listed = server._methods["workers.list"](2, {})
    assert [worker["worker_id"] for worker in listed["result"]["workers"]] == [
        "office-seo"
    ]

    now = time.time()
    fresh_db.ensure_session(
        "office-office-seo",
        source="subagent",
        model="gpt-office",
        parent_session_id="parent-123",
    )
    fresh_db.update_session_billing_route(
        "office-office-seo",
        provider="openai",
        base_url="https://api.openai.com/v1",
    )

    def _seed_review(conn):
        conn.execute(
            "INSERT INTO delegate_tasks "
            "(id, parent_session_id, worker_role, worker_id, goal, status, "
            "handoff_mode, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "review-task",
                "parent-123",
                "seo",
                "office-seo",
                "Review the launch",
                "waiting_approval",
                "smart",
                now,
                now,
            ),
        )
        conn.execute(
            "INSERT INTO delegate_task_attempts "
            "(id, task_id, attempt_number, child_session_id, status, result, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "review-attempt",
                "review-task",
                1,
                "office-office-seo",
                "waiting_approval",
                "Launch review complete",
                now,
            ),
        )

    fresh_db._execute_write(_seed_review)
    tasks = server._methods["tasks.list"](3, {"status": "waiting_approval"})
    assert tasks["result"]["tasks"][0]["worker_name"] == "Office SEO"
    assert tasks["result"]["tasks"][0]["result"] == "Launch review complete"
    assert tasks["result"]["tasks"][0]["child_session_id"] == "office-office-seo"
    assert tasks["result"]["tasks"][0]["execution_model"] == "gpt-office"
    assert tasks["result"]["tasks"][0]["execution_provider"] == "openai"

    approved = server._methods["tasks.approve"](4, {"task_id": "review-task"})
    assert approved["result"]["success"] is True
    with fresh_db._read_ctx() as conn:
        status = conn.execute(
            "SELECT status FROM delegate_tasks WHERE id = ?", ("review-task",)
        ).fetchone()[0]
    assert status == "completed"
    fresh_db.close()


def test_worker_supervisor_inherits_profile_runtime_and_parent_session(
    fresh_db, monkeypatch
):
    from agent.agent_registry import get_agent_template
    from agent.secret_scope import current_secret_scope
    from pixel_constants import get_pixel_agents_home_override
    import run_agent

    db = fresh_db
    worker = db.hire_worker("runtime-worker", "seo-specialist", "Runtime SEO")
    template = get_agent_template(worker.template_id)
    profile_home = Path(db.db_path).parent
    (profile_home / ".env").write_text("OFFICE_TEST_SECRET=scoped-value\n")

    credential_pool = object()
    captured = {}

    class FakeAgent:
        def __init__(self, **kwargs):
            captured["kwargs"] = kwargs
            captured["profile_home"] = get_pixel_agents_home_override()
            captured["secret"] = (current_secret_scope() or {}).get(
                "OFFICE_TEST_SECRET"
            )
            self.provider = kwargs["provider"]
            self.model = kwargs["model"]
            self._session_init_model_config = {}

        def run_conversation(self, **kwargs):
            captured["run"] = kwargs
            return {"completed": True, "final_response": "worker result"}

    monkeypatch.setattr(run_agent, "AIAgent", FakeAgent)
    monkeypatch.setattr(
        WorkerSupervisor,
        "_resolve_worker_runtime",
        lambda self, parent_session_id: (
            {
                "model": "gpt-worker",
                "provider": "openai",
                "requested_provider": "openai",
                "base_url": "https://api.openai.com/v1",
                "api_key": "profile-key",
                "api_mode": "codex_responses",
                "credential_pool": credential_pool,
            },
            {"delegation": {"max_iterations": 17}},
        ),
    )

    result = WorkerSupervisor(db=db)._run_agent_sync(
        worker,
        template,
        "runtime-task",
        "Audit the site",
        parent_session_id="parent-123",
    )

    kwargs = captured["kwargs"]
    assert kwargs["session_db"] is db
    assert kwargs["parent_session_id"] == "parent-123"
    assert kwargs["provider"] == "openai"
    assert kwargs["model"] == "gpt-worker"
    assert kwargs["api_key"] == "profile-key"
    assert kwargs["credential_pool"] is credential_pool
    assert kwargs["max_iterations"] == 17
    assert captured["profile_home"] == str(profile_home.resolve())
    assert captured["secret"] == "scoped-value"
    assert result["execution"]["worker_id"] == "runtime-worker"
    assert result["execution"]["provider"] == "openai"
    assert get_pixel_agents_home_override() is None


def test_worker_runtime_uses_parent_model_and_provider(fresh_db, monkeypatch):
    from agent.worker_supervisor import WorkerSupervisor
    import pixel_cli.runtime_provider as runtime_provider
    import pixel_cli.config as config

    fresh_db._execute_write(
        lambda conn: conn.execute(
            "UPDATE sessions SET model = ?, billing_provider = ?, billing_base_url = ? "
            "WHERE id = ?",
            (
                "parent-model",
                "openai",
                "https://api.openai.com/v1",
                "parent-123",
            ),
        )
    )
    monkeypatch.setattr(
        config,
        "load_config_readonly",
        lambda: {"model": {"default": "profile-default", "provider": "anthropic"}},
    )
    captured = {}

    def fake_resolve_runtime_provider(**kwargs):
        captured.update(kwargs)
        return {
            "provider": "openai",
            "requested_provider": "openai",
            "base_url": "https://api.openai.com/v1",
            "api_key": "resolved-profile-key",
        }

    monkeypatch.setattr(
        runtime_provider, "resolve_runtime_provider", fake_resolve_runtime_provider
    )

    runtime, _ = WorkerSupervisor(db=fresh_db)._resolve_worker_runtime("parent-123")
    assert captured["requested"] == "openai"
    assert captured["target_model"] == "parent-model"
    assert runtime["model"] == "parent-model"


def test_office_worker_error_text_is_never_classified_as_completed():
    from tools.delegate_tool import _delegated_result_status

    result = {
        "completed": False,
        "final_response": "No LLM provider configured",
        "error": "The assigned office worker failed.",
        "office_task_queued": True,
        "office_task_status": "error",
    }
    assert _delegated_result_status(
        result,
        summary=result["final_response"],
        interrupted=False,
        empty_sentinel=False,
    ) == "failed"


@pytest.mark.asyncio
async def test_runtime_resolution_failure_is_persisted_as_worker_error(
    fresh_db, monkeypatch
):
    db = fresh_db
    db.hire_worker("broken-runtime", "seo-specialist", "Broken Runtime")
    db.update_worker("broken-runtime", {"status": "idle"})
    now = time.time()
    db._execute_write(
        lambda conn: conn.execute(
            "INSERT INTO delegate_tasks "
            "(id, parent_session_id, worker_role, worker_id, goal, status, "
            "handoff_mode, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "broken-task",
                "parent-123",
                "seo",
                "broken-runtime",
                "Audit the page",
                "queued",
                "smart",
                now,
                now,
            ),
        )
    )
    supervisor = WorkerSupervisor(db=db)
    monkeypatch.setattr(
        supervisor,
        "_run_agent_sync",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("LLM runtime for the assigned worker could not be resolved")
        ),
    )

    pending = await supervisor._poll_queue()
    await asyncio.gather(*pending)

    with db._read_ctx() as conn:
        task = conn.execute(
            "SELECT status FROM delegate_tasks WHERE id = ?", ("broken-task",)
        ).fetchone()
        attempt = conn.execute(
            "SELECT status, result FROM delegate_task_attempts WHERE task_id = ?",
            ("broken-task",),
        ).fetchone()
        worker = conn.execute(
            "SELECT status FROM workers WHERE worker_id = ?", ("broken-runtime",)
        ).fetchone()
    assert task["status"] == "error"
    assert attempt["status"] == "error"
    assert "LLM runtime" in attempt["result"]
    assert worker["status"] == "error"


@pytest.mark.asyncio
async def test_office_e2e(fresh_db, monkeypatch):
    """
    End-to-End Test for the Autonomous AI Office workflow:
    1. Hire a worker
    2. Enqueue a task for the worker
    3. Supervisor executes the task (mocked agent run)
    4. Task goes to waiting_approval
    5. User rejects the task
    6. Task goes back to queued
    """
    db = fresh_db

    # 1. Hire a worker
    worker = db.hire_worker("test-worker-1", "seo-specialist", "SEO Bob", "smart")
    assert worker.worker_id == "test-worker-1"
    assert worker.status == "onboarding"

    # Update to idle
    db.update_worker("test-worker-1", {"status": "idle"})
    assert db.get_worker("test-worker-1").status == "idle"

    # 2. Enqueue a task
    def _insert_task(conn):
        now = time.time()
        conn.execute(
            "INSERT INTO delegate_tasks (id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "task-1",
                "parent-123",
                "seo",
                "test-worker-1",
                "Analyze the homepage",
                "queued",
                "smart",
                now,
                now,
            ),
        )

    db._execute_write(_insert_task)

    # 3. Supervisor executes the task
    supervisor = WorkerSupervisor(db=db)

    # Mock the AIAgent execution in supervisor to avoid real LLM calls
    def mock_run_agent_sync(*args, **kwargs):
        return {"final_response": "Here is the SEO analysis", "completed": True}

    monkeypatch.setattr(supervisor, "_run_agent_sync", mock_run_agent_sync)

    # Run one poll loop
    pending = await supervisor._poll_queue()
    await asyncio.gather(*pending)

    # 4. Verify task is in waiting_approval
    with db._read_ctx() as conn:
        task = conn.execute(
            "SELECT * FROM delegate_tasks WHERE id = 'task-1'"
        ).fetchone()
        assert task["status"] == "waiting_approval"

        attempt = conn.execute(
            "SELECT * FROM delegate_task_attempts WHERE task_id = 'task-1'"
        ).fetchone()
        assert attempt["result"] == "Here is the SEO analysis"
        assert attempt["status"] == "waiting_approval"

    # 5. User rejects the task (via tui_gateway methods)
    from tui_gateway import server

    reject_handler = server._methods["tasks.reject"]
    response = reject_handler(
        1, {"task_id": "task-1", "feedback": "Need more keywords"}
    )

    assert response["result"]["success"] is True

    # 6. Verify task is back to queued and attempt is rejected
    with db._read_ctx() as conn:
        task = conn.execute(
            "SELECT * FROM delegate_tasks WHERE id = 'task-1'"
        ).fetchone()
        assert task["status"] == "queued"

        attempt = conn.execute(
            "SELECT * FROM delegate_task_attempts WHERE task_id = 'task-1'"
        ).fetchone()
    assert attempt["status"] == "rejected"
    assert attempt["review_feedback"] == "Need more keywords"
    db.close()


@pytest.mark.asyncio
async def test_autonomous_worker_serializes_tasks_and_recovers_stale_claim(
    fresh_db, monkeypatch
):
    db = fresh_db
    db.hire_worker("autonomous-1", "seo-specialist", "SEO Auto", "autonomous")
    db.update_worker("autonomous-1", {"status": "working"})

    stale = time.time() - 3600
    now = time.time()

    def _seed(conn):
        conn.execute(
            "INSERT INTO delegate_tasks "
            "(id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "stale-task",
                "parent-123",
                "seo",
                "autonomous-1",
                "First",
                "working",
                "autonomous",
                stale,
                stale,
            ),
        )
        conn.execute(
            "INSERT INTO delegate_tasks "
            "(id, parent_session_id, worker_role, worker_id, goal, status, handoff_mode, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "next-task",
                "parent-123",
                "seo",
                "autonomous-1",
                "Second",
                "queued",
                "autonomous",
                now,
                now,
            ),
        )

    db._execute_write(_seed)
    supervisor = WorkerSupervisor(db=db, claim_timeout=1)
    monkeypatch.setattr(
        supervisor,
        "_run_agent_sync",
        lambda *args, **kwargs: {"final_response": "done", "completed": True},
    )

    first_batch = await supervisor._poll_queue()
    assert len(first_batch) == 1
    await asyncio.gather(*first_batch)
    second_batch = await supervisor._poll_queue()
    assert len(second_batch) == 1
    await asyncio.gather(*second_batch)

    with db._read_ctx() as conn:
        statuses = dict(
            conn.execute("SELECT id, status FROM delegate_tasks").fetchall()
        )
        attempts = conn.execute(
            "SELECT COUNT(*) FROM delegate_task_attempts"
        ).fetchone()[0]
    assert statuses == {"stale-task": "completed", "next-task": "completed"}
    assert attempts == 2
    db.close()
