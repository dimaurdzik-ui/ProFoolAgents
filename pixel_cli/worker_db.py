import sqlite3
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

from pixel_constants import get_pixel_agents_home

def connect(profile: Optional[str] = None) -> sqlite3.Connection:
    home_dir = get_pixel_agents_home()
    if profile:
        db_path = home_dir / f"workers_{profile}.db"
    else:
        db_path = home_dir / "workers.db"
    
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    # Enable WAL mode for concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    
    _init_schema(conn)
    return conn

def _init_schema(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workers (
        worker_id     TEXT PRIMARY KEY,
        template_id   TEXT NOT NULL,
        display_name  TEXT NOT NULL,
        autonomy_mode TEXT NOT NULL DEFAULT 'smart',
        status        TEXT NOT NULL DEFAULT 'idle',
        manager_id    TEXT,
        created_at    INTEGER NOT NULL,
        archived_at   INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id                   TEXT PRIMARY KEY,
        worker_id            TEXT NOT NULL,
        goal                 TEXT NOT NULL,
        deliverable          TEXT,
        acceptance_criteria  TEXT,
        priority             TEXT NOT NULL DEFAULT 'normal',
        deadline_at          INTEGER,
        status               TEXT NOT NULL DEFAULT 'queued',
        result               TEXT,
        last_error           TEXT,
        retry_count          INTEGER NOT NULL DEFAULT 0,
        max_retries          INTEGER NOT NULL DEFAULT 3,
        created_at           INTEGER NOT NULL,
        updated_at           INTEGER NOT NULL,
        pending_tool_name    TEXT,
        pending_tool_args    TEXT,
        FOREIGN KEY(worker_id) REFERENCES workers(worker_id)
    )
    """)
    
    # Simple migration for existing DBs
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN pending_tool_name TEXT")
        cursor.execute("ALTER TABLE tasks ADD COLUMN pending_tool_args TEXT")
    except sqlite3.OperationalError:
        pass
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_events (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id    TEXT NOT NULL,
        event_type TEXT NOT NULL,
        payload    TEXT,
        created_at INTEGER NOT NULL
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_worker ON tasks(worker_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_task ON task_events(task_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_cursor ON task_events(id)")
    conn.commit()

def hire_worker(conn: sqlite3.Connection, worker_id: str, template_id: str, display_name: str, autonomy_mode: str = 'smart', manager_id: Optional[str] = None):
    cursor = conn.cursor()
    now = int(time.time() * 1000)
    cursor.execute("""
        INSERT INTO workers (worker_id, template_id, display_name, autonomy_mode, status, manager_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (worker_id, template_id, display_name, autonomy_mode, 'idle', manager_id, now))
    conn.commit()
    return dict(cursor.execute("SELECT * FROM workers WHERE worker_id = ?", (worker_id,)).fetchone())

def list_workers(conn: sqlite3.Connection, include_archived: bool = False) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    if include_archived:
        cursor.execute("SELECT * FROM workers ORDER BY created_at DESC")
    else:
        cursor.execute("SELECT * FROM workers WHERE archived_at IS NULL ORDER BY created_at DESC")
    return [dict(row) for row in cursor.fetchall()]

def update_worker(conn: sqlite3.Connection, worker_id: str, **updates):
    if not updates:
        return
    
    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [worker_id]
    
    cursor = conn.cursor()
    cursor.execute(f"UPDATE workers SET {set_clause} WHERE worker_id = ?", values)
    conn.commit()

def archive_worker(conn: sqlite3.Connection, worker_id: str):
    update_worker(conn, worker_id, archived_at=int(time.time() * 1000))

def create_task(conn: sqlite3.Connection, task_id: str, worker_id: str, goal: str, **kwargs):
    cursor = conn.cursor()
    now = int(time.time() * 1000)
    
    deliverable = kwargs.get('deliverable')
    acceptance_criteria = json.dumps(kwargs.get('acceptance_criteria', [])) if kwargs.get('acceptance_criteria') else None
    priority = kwargs.get('priority', 'normal')
    deadline_at = kwargs.get('deadline_at')
    
    cursor.execute("""
        INSERT INTO tasks (id, worker_id, goal, deliverable, acceptance_criteria, priority, deadline_at, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (task_id, worker_id, goal, deliverable, acceptance_criteria, priority, deadline_at, 'queued', now, now))
    
    # Emit event
    _emit_event(cursor, task_id, 'status_change', {'status': 'queued'})
    
    conn.commit()
    return dict(cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone())

def list_tasks(conn: sqlite3.Connection, worker_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    conditions = []
    params = []
    
    if worker_id:
        conditions.append("worker_id = ?")
        params.append(worker_id)
    if status:
        conditions.append("status = ?")
        params.append(status)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY created_at DESC"
    cursor.execute(query, tuple(params))
    return [dict(row) for row in cursor.fetchall()]

def update_task(conn: sqlite3.Connection, task_id: str, emit_event_type: Optional[str] = None, **updates):
    if not updates:
        return
    
    now = int(time.time() * 1000)
    updates['updated_at'] = now
    
    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [task_id]
    
    cursor = conn.cursor()
    cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
    
    if emit_event_type:
        payload = updates.copy()
        if 'updated_at' in payload:
            del payload['updated_at']
        _emit_event(cursor, task_id, emit_event_type, payload)
    
    conn.commit()

def _emit_event(cursor: sqlite3.Cursor, task_id: str, event_type: str, payload: Dict[str, Any]):
    now = int(time.time() * 1000)
    cursor.execute("""
        INSERT INTO task_events (task_id, event_type, payload, created_at)
        VALUES (?, ?, ?, ?)
    """, (task_id, event_type, json.dumps(payload), now))

def tail_events(conn: sqlite3.Connection, cursor_id: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM task_events 
        WHERE id > ? 
        ORDER BY id ASC 
        LIMIT ?
    """, (cursor_id, limit))
    return [dict(row) for row in cursor.fetchall()]
