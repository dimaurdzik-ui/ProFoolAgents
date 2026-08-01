import time
from typing import List, Optional, Dict, Any

from agent.workers import WorkerInstance

WORKER_STATUSES = frozenset({"onboarding", "idle", "working", "paused", "archived", "error"})
AUTONOMY_MODES = frozenset({"manual", "smart", "autonomous"})

class SessionWorkersMixin:
    """Mixin for SessionDB to handle workers and delegate_tasks tables."""

    def hire_worker(self, worker_id: str, template_id: str, display_name: str, autonomy_mode: str = "smart", manager_id: Optional[str] = None) -> WorkerInstance:
        if autonomy_mode not in AUTONOMY_MODES:
            raise ValueError(f"Invalid autonomy_mode: {autonomy_mode}")
        now = time.time()
        def _insert(conn):
            conn.execute(
                "INSERT INTO workers (worker_id, template_id, display_name, status, autonomy_mode, manager_id, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (worker_id, template_id, display_name, "onboarding", autonomy_mode, manager_id, now)
            )
        self._execute_write(_insert)
        return WorkerInstance(worker_id, template_id, display_name, "onboarding", autonomy_mode, manager_id, now, None)

    def get_worker(self, worker_id: str) -> Optional[WorkerInstance]:
        with self._read_ctx() as conn:
            row = conn.execute("SELECT * FROM workers WHERE worker_id = ?", (worker_id,)).fetchone()
            if not row:
                return None
            return WorkerInstance(
                worker_id=row["worker_id"],
                template_id=row["template_id"],
                display_name=row["display_name"],
                status=row["status"],
                autonomy_mode=row["autonomy_mode"],
                manager_id=row["manager_id"],
                created_at=row["created_at"],
                archived_at=row["archived_at"],
            )

    def list_workers(self, include_archived: bool = False) -> List[WorkerInstance]:
        with self._read_ctx() as conn:
            if include_archived:
                rows = conn.execute("SELECT * FROM workers ORDER BY created_at DESC").fetchall()
            else:
                rows = conn.execute("SELECT * FROM workers WHERE archived_at IS NULL ORDER BY created_at DESC").fetchall()

            return [
                WorkerInstance(
                    worker_id=row["worker_id"],
                    template_id=row["template_id"],
                    display_name=row["display_name"],
                    status=row["status"],
                    autonomy_mode=row["autonomy_mode"],
                    manager_id=row["manager_id"],
                    created_at=row["created_at"],
                    archived_at=row["archived_at"],
                ) for row in rows
            ]

    def find_worker_by_template(self, template_id: str) -> Optional[WorkerInstance]:
        """Return the oldest active instance for a profession template."""
        with self._read_ctx() as conn:
            row = conn.execute(
                "SELECT * FROM workers WHERE template_id = ? AND archived_at IS NULL "
                "AND status IN ('onboarding', 'idle', 'working') "
                "ORDER BY created_at LIMIT 1",
                (template_id,),
            ).fetchone()
        return self.get_worker(row["worker_id"]) if row else None

    def update_worker(self, worker_id: str, updates: Dict[str, Any]) -> bool:
        if not updates:
            return True
        allowed_keys = {"display_name", "status", "autonomy_mode", "manager_id"}
        if "status" in updates and updates["status"] not in WORKER_STATUSES:
            raise ValueError(f"Invalid worker status: {updates['status']}")
        if "autonomy_mode" in updates and updates["autonomy_mode"] not in AUTONOMY_MODES:
            raise ValueError(f"Invalid autonomy_mode: {updates['autonomy_mode']}")
        set_clauses = []
        params = []
        for k, v in updates.items():
            if k in allowed_keys:
                set_clauses.append(f"{k} = ?")
                params.append(v)

        if not set_clauses:
            return False

        params.append(worker_id)
        def _update(conn):
            cursor = conn.execute(f"UPDATE workers SET {', '.join(set_clauses)} WHERE worker_id = ?", params)
            return cursor.rowcount > 0
        return self._execute_write(_update)

    def archive_worker(self, worker_id: str) -> bool:
        now = time.time()
        def _archive(conn):
            cursor = conn.execute(
                "UPDATE workers SET archived_at = ?, status = 'archived' "
                "WHERE worker_id = ? AND status != 'working'",
                (now, worker_id),
            )
            if cursor.rowcount:
                conn.execute(
                    "UPDATE delegate_tasks SET status = 'error', updated_at = ? "
                    "WHERE worker_id = ? AND status = 'queued'",
                    (now, worker_id),
                )
            return cursor.rowcount > 0
        return self._execute_write(_archive)

    def unarchive_worker(self, worker_id: str) -> bool:
        def _unarchive(conn):
            cursor = conn.execute(
                "UPDATE workers SET archived_at = NULL, status = 'idle' WHERE worker_id = ?",
                (worker_id,),
            )
            return cursor.rowcount > 0
        return self._execute_write(_unarchive)
