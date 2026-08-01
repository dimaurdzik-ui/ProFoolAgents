import asyncio
import pytest
from unittest.mock import patch, MagicMock

from pixel_cli.worker_runner import WorkerRunner
from pixel_cli.worker_db import connect, hire_worker, create_task, update_worker

@pytest.fixture
def db_conn():
    conn = connect(profile="test_runner")
    yield conn
    conn.close()

@pytest.mark.asyncio
@patch('pixel_cli.worker_runner.AIAgent')
async def test_spawn_creates_session(MockAIAgent, db_conn):
    # Setup
    hire_worker(db_conn, "w1", "researcher", "Researcher", "smart")
    task = create_task(db_conn, "t1", "w1", "Find something")
    
    # Mock
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_conversation.return_value = {"final_response": "Done!"}
    MockAIAgent.return_value = mock_agent_instance
    
    # Execute
    runner = WorkerRunner(db_profile="test_runner")
    await runner._run_worker_task("w1", "t1")
    
    # Assert
    MockAIAgent.assert_called_once()
    args, kwargs = MockAIAgent.call_args
    assert kwargs.get("session_id") == "worker-w1"
    
    cursor = db_conn.cursor()
    updated_task = cursor.execute("SELECT * FROM tasks WHERE id = 't1'").fetchone()
    assert updated_task["status"] == "waiting_approval"
    assert updated_task["result"] == "Done!"

@pytest.mark.asyncio
@patch('pixel_cli.worker_runner.AIAgent')
async def test_reject_sends_feedback_message(MockAIAgent, db_conn):
    # Setup
    hire_worker(db_conn, "w1", "researcher", "Researcher", "smart")
    create_task(db_conn, "t1", "w1", "Find something")
    
    # Mock
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_conversation.return_value = {"final_response": "Fixed!"}
    MockAIAgent.return_value = mock_agent_instance
    
    # Execute
    runner = WorkerRunner(db_profile="test_runner")
    await runner._retry_worker_task("t1", "Not good enough")
    
    # Assert
    mock_agent_instance.run_conversation.assert_called_once()
    args, kwargs = mock_agent_instance.run_conversation.call_args
    assert "Not good enough" in kwargs.get("user_message", "")
    
    cursor = db_conn.cursor()
    updated_task = cursor.execute("SELECT * FROM tasks WHERE id = 't1'").fetchone()
    assert updated_task["retry_count"] == 1
    assert updated_task["status"] == "waiting_approval"

@pytest.mark.asyncio
@patch('pixel_cli.worker_runner.AIAgent')
async def test_autonomy_mode_blocks_approval(MockAIAgent, db_conn):
    # Setup autonomous worker
    hire_worker(db_conn, "w2", "researcher", "Autonomous", "autonomous")
    create_task(db_conn, "t2", "w2", "Do autonomous work")
    
    # Mock
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_conversation.return_value = {"final_response": "Finished!"}
    MockAIAgent.return_value = mock_agent_instance
    
    # Execute
    runner = WorkerRunner(db_profile="test_runner")
    await runner._run_worker_task("w2", "t2")
    
    # Assert
    cursor = db_conn.cursor()
    updated_task = cursor.execute("SELECT * FROM tasks WHERE id = 't2'").fetchone()
    assert updated_task["status"] == "done"  # Not waiting_approval!
