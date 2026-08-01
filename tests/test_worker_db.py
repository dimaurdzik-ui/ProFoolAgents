import os
import tempfile
import pytest
from pathlib import Path

from pixel_cli.worker_db import connect, hire_worker, list_workers, create_task, update_task, tail_events, archive_worker

@pytest.fixture
def db_conn():
    # Use in-memory db for tests by patching get_pixel_agents_home or connecting directly
    # To keep it simple without patching constants, we'll just test the logic with a profile
    conn = connect(profile="test_workers")
    yield conn
    conn.close()
    
    # cleanup
    from pixel_constants import get_pixel_agents_home
    home = get_pixel_agents_home()
    db_file = home / "workers_test_workers.db"
    if db_file.exists():
        os.remove(db_file)

def test_hire_and_list_worker(db_conn):
    worker = hire_worker(db_conn, "w1", "seo-specialist", "SEO Guru", "smart")
    assert worker["worker_id"] == "w1"
    
    workers = list_workers(db_conn)
    assert len(workers) == 1
    assert workers[0]["worker_id"] == "w1"
    
    archive_worker(db_conn, "w1")
    
    workers_no_archived = list_workers(db_conn, include_archived=False)
    assert len(workers_no_archived) == 0
    
    workers_all = list_workers(db_conn, include_archived=True)
    assert len(workers_all) == 1

def test_create_and_approve_task(db_conn):
    hire_worker(db_conn, "w1", "t1", "W1", "smart")
    
    task = create_task(db_conn, "task1", "w1", "Do something")
    assert task["status"] == "queued"
    assert task["worker_id"] == "w1"
    
    update_task(db_conn, "task1", emit_event_type="status_change", status="approved")
    
    cursor = db_conn.cursor()
    updated = cursor.execute("SELECT * FROM tasks WHERE id = 'task1'").fetchone()
    assert updated["status"] == "approved"

def test_reject_increments_retry(db_conn):
    hire_worker(db_conn, "w1", "t1", "W1", "smart")
    create_task(db_conn, "task1", "w1", "Do something")
    
    update_task(db_conn, "task1", retry_count=1)
    
    cursor = db_conn.cursor()
    updated = cursor.execute("SELECT * FROM tasks WHERE id = 'task1'").fetchone()
    assert updated["retry_count"] == 1

def test_tail_events_returns_new_rows(db_conn):
    hire_worker(db_conn, "w1", "t1", "W1", "smart")
    create_task(db_conn, "task1", "w1", "Do something")
    
    events1 = tail_events(db_conn, cursor_id=0)
    assert len(events1) >= 1
    
    last_id = events1[-1]["id"]
    
    update_task(db_conn, "task1", emit_event_type="status_change", status="working")
    
    events2 = tail_events(db_conn, cursor_id=last_id)
    assert len(events2) == 1
    assert events2[0]["event_type"] == "status_change"
