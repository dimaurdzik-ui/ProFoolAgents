import asyncio
import atexit
import json
import logging
import threading
import time
import uuid
from pathlib import Path
import weakref
from typing import Optional

from pixel_state import SessionDB
from agent.agent_registry import get_agent_template

logger = logging.getLogger(__name__)
_supervisor_db_lock = threading.Lock()

class WorkerSupervisor:
    active_agents = weakref.WeakValueDictionary()
    
    def __init__(
        self,
        poll_interval: float = 2.0,
        db: Optional[SessionDB] = None,
        claim_timeout: float = 900.0,
        heartbeat_interval: float = 30.0,
    ):
        self.poll_interval = poll_interval
        self.db = db or SessionDB()
        self.claim_timeout = claim_timeout
        self.heartbeat_interval = heartbeat_interval
        self._running = False
        self._active_tasks: set[asyncio.Task] = set()
        self._last_recovery = 0.0

    async def start(self):
        self._running = True
        logger.info("WorkerSupervisor started")
        while self._running:
            try:
                await self._poll_queue()
            except Exception as e:
                logger.error(f"Supervisor loop error: {e}")
            await asyncio.sleep(self.poll_interval)

    def stop(self):
        self._running = False

    def close(self):
        self.stop()
        try:
            self.db.close()
        except Exception:
            pass

    async def _poll_queue(self) -> list[asyncio.Task]:
        now = time.monotonic()
        if now - self._last_recovery >= min(60.0, self.claim_timeout / 2):
            await asyncio.to_thread(self._recover_stale_claims)
            self._last_recovery = now
            
        def _fetch_and_claim():
            with self.db._read_ctx() as conn:
                tasks = conn.execute(
                    "SELECT t.id, t.parent_session_id, t.worker_id, t.worker_role, "
                    "t.goal, t.status, t.dependencies_json, "
                    "t.deliverable, t.acceptance_criteria "
                    "FROM delegate_tasks t "
                    "WHERE t.status = 'queued' "
                    "ORDER BY t.priority DESC, t.created_at"
                ).fetchall()
            
            if not tasks:
                return []
                
            claimed = []
            for t_row in tasks:
                task_id = t_row["id"]
                worker_id = t_row["worker_id"]
                task = dict(t_row)
                
                # Check dependencies
                deps_json = task.get("dependencies_json")
                if deps_json:
                    try:
                        deps = json.loads(deps_json)
                    except Exception as e:
                        logger.error(f"Task {task_id}: malformed dependencies JSON. Marking as error.")
                        def _mark_error(conn, err=e):
                            conn.execute("UPDATE delegate_tasks SET status = 'error', error_text = ? WHERE id = ?", (f"Malformed dependencies JSON: {err}", task_id))
                        self.db._execute_write(_mark_error)
                        continue
                        
                    if deps:
                        if task_id in deps:
                            def _mark_self(conn):
                                conn.execute("UPDATE delegate_tasks SET status = 'error', error_text = ? WHERE id = ?", ("Self dependency detected.", task_id))
                            self.db._execute_write(_mark_self)
                            continue
                            
                        # Fetch all dependency statuses
                        with self.db._read_ctx() as conn:
                            placeholders = ",".join("?" for _ in deps)
                            rows = conn.execute(
                                f"SELECT id, status FROM delegate_tasks WHERE id IN ({placeholders})",
                                deps
                            ).fetchall()
                        
                        dep_statuses = {r["id"]: r["status"] for r in rows}
                        missing = [d for d in deps if d not in dep_statuses]
                        if missing:
                            def _mark_missing(conn, m=missing):
                                conn.execute("UPDATE delegate_tasks SET status = 'error', error_text = ? WHERE id = ?", (f"Missing dependencies: {m}", task_id))
                            self.db._execute_write(_mark_missing)
                            continue
                            
                        failed_deps = [d for d, s in dep_statuses.items() if s in ('error', 'failed')]
                        if failed_deps:
                            def _mark_failed(conn, f=failed_deps):
                                conn.execute("UPDATE delegate_tasks SET status = 'error', error_text = ? WHERE id = ?", (f"Dependency failed: {f}", task_id))
                            self.db._execute_write(_mark_failed)
                            continue
                            
                        unfinished = [d for d, s in dep_statuses.items() if s != 'completed']
                        if unfinished:
                            # Cycle detection
                            with self.db._read_ctx() as conn:
                                all_deps_rows = conn.execute(
                                    "SELECT id, dependencies_json FROM delegate_tasks WHERE status != 'completed' AND dependencies_json IS NOT NULL"
                                ).fetchall()
                            
                            graph = {}
                            for r in all_deps_rows:
                                try:
                                    g_deps = json.loads(r["dependencies_json"])
                                    if isinstance(g_deps, list):
                                        graph[r["id"]] = g_deps
                                except Exception:
                                    pass
                            
                            def has_cycle(start_node):
                                visited = set()
                                stack = set()
                                def dfs(node):
                                    if node in stack:
                                        return True
                                    if node in visited:
                                        return False
                                    visited.add(node)
                                    stack.add(node)
                                    for neighbor in graph.get(node, []):
                                        if dfs(neighbor):
                                            return True
                                    stack.remove(node)
                                    return False
                                return dfs(start_node)

                            if has_cycle(task_id):
                                def _mark_cycle(conn):
                                    conn.execute("UPDATE delegate_tasks SET status = 'error', error_text = ? WHERE id = ?", ("Cyclic dependency detected.", task_id))
                                self.db._execute_write(_mark_cycle)
                                continue

                            # Still blocked by dependencies, wait for them to finish
                            continue
                
                if not worker_id:
                    # Find an idle worker of this role
                    with self.db._read_ctx() as conn:
                        row = conn.execute(
                            "SELECT worker_id, autonomy_mode FROM workers "
                            "WHERE template_id = ? AND status IN ('idle', 'onboarding') AND archived_at IS NULL "
                            "LIMIT 1",
                            (task["worker_role"],)
                        ).fetchone()
                    if row:
                        worker_id = row["worker_id"]
                        task["worker_id"] = worker_id
                        task["autonomy_mode"] = row["autonomy_mode"]
                    else:
                        continue
                else:
                    with self.db._read_ctx() as conn:
                        row = conn.execute(
                            "SELECT status, autonomy_mode FROM workers WHERE worker_id = ? AND archived_at IS NULL",
                            (worker_id,)
                        ).fetchone()
                    if not row or row["status"] not in ('idle', 'onboarding'):
                        continue
                    task["autonomy_mode"] = row["autonomy_mode"]
                
                def _claim(conn, w_id, t_id):
                    cursor = conn.execute(
                        "UPDATE delegate_tasks SET status = 'working', worker_id = ?, updated_at = ? "
                        "WHERE id = ? AND status = 'queued' AND NOT EXISTS ("
                        "SELECT 1 FROM delegate_tasks active WHERE active.worker_id = ? "
                        "AND active.status = 'working' AND active.id != ?)",
                        (w_id, time.time(), t_id, w_id, t_id),
                    )
                    if cursor.rowcount:
                        conn.execute(
                            "UPDATE workers SET status = 'working' WHERE worker_id = ? "
                            "AND archived_at IS NULL AND status IN ('idle', 'onboarding')",
                            (w_id,),
                        )
                    return cursor.rowcount > 0
                
                with _supervisor_db_lock:
                    if self.db._execute_write(lambda conn: _claim(conn, worker_id, task_id)):
                        claimed.append(task)
                        if len(claimed) >= 5:
                            break
            return claimed

        claimed_tasks = await asyncio.to_thread(_fetch_and_claim)

        created_tasks: list[asyncio.Task] = []
        for task in claimed_tasks:
            worker_id = task["worker_id"]
            logger.info(f"WorkerSupervisor: Assigned task {task['id']} to worker {worker_id}")
            pending = asyncio.create_task(self._execute_worker_task(task))
            self._active_tasks.add(pending)
            pending.add_done_callback(self._active_tasks.discard)
            created_tasks.append(pending)
        return created_tasks

    async def _execute_worker_task(self, task: dict):
        task_id = task["id"]
        worker_id = task["worker_id"]
        goal = task["goal"]
        deliverable = task.get("deliverable")
        raw_criteria = task.get("acceptance_criteria")
        try:
            acceptance_criteria = json.loads(raw_criteria) if raw_criteria else []
        except (TypeError, json.JSONDecodeError):
            acceptance_criteria = []

        worker = self.db.get_worker(worker_id)
        if not worker:
            logger.error(f"Worker {worker_id} not found for task {task_id}")
            self._fail_task(task_id, "Worker not found")
            return

        template = get_agent_template(worker.template_id)
        if not template:
            self._fail_task(task_id, "Template not found")
            return

        loop = asyncio.get_running_loop()
        heartbeat = asyncio.create_task(self._heartbeat_claim(task_id))
        try:
            result = await loop.run_in_executor(
                None,
                self._run_agent_sync,
                worker,
                template,
                task_id,
                goal,
                deliverable,
                acceptance_criteria,
                task.get("parent_session_id"),
            )

            def _complete(conn):
                now = time.time()
                attempt_id = "attempt-" + uuid.uuid4().hex[:8]
                # get max attempt number
                row = conn.execute("SELECT MAX(attempt_number) as max_attempt FROM delegate_task_attempts WHERE task_id = ?", (task_id,)).fetchone()
                attempt_num = (row["max_attempt"] or 0) + 1

                successful = bool(result.get("completed", True)) and not result.get("error")
                next_status = (
                    "completed"
                    if successful and worker.autonomy_mode == "autonomous"
                    else "waiting_approval" if successful else "error"
                )
                child_session_id = f"office-{worker.worker_id}"
                session_exists = conn.execute(
                    "SELECT 1 FROM sessions WHERE id = ?", (child_session_id,)
                ).fetchone()
                conn.execute(
                    "INSERT INTO delegate_task_attempts "
                    "(id, task_id, attempt_number, child_session_id, status, result, acceptance_check, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        attempt_id,
                        task_id,
                        attempt_num,
                        child_session_id if session_exists else None,
                        next_status,
                        result.get("final_response", ""),
                        result.get("acceptance_check_json"),
                        now,
                    ),
                )
                conn.execute(
                    "UPDATE delegate_tasks SET status = ?, updated_at = ?, completed_at = ?, result_json = ? WHERE id = ?",
                    (
                        next_status, 
                        now, 
                        now if next_status in ('completed', 'error') else None,
                        json.dumps(result) if next_status in ('completed', 'error') else None,
                        task_id
                    ),
                )
                conn.execute(
                    "UPDATE workers SET status = ? WHERE worker_id = ? AND archived_at IS NULL",
                    ("idle" if successful else "error", worker_id),
                )
                return next_status
            with _supervisor_db_lock:
                next_status = self.db._execute_write(_complete)
            logger.info("WorkerSupervisor: Task %s entered %s", task_id, next_status)

            parent = task.get("parent_session_id")
            successful = bool(result.get("completed", True)) and not result.get("error")
            try:
                from agent.office_events import enqueue_office_completion

                enqueue_office_completion(
                    self.db,
                    parent_session_id=parent,
                    task_id=task_id,
                    worker_id=worker_id,
                    goal=goal,
                    status="completed" if successful else "error",
                    summary=result.get("final_response", ""),
                    error=result.get("error", ""),
                )
            except Exception:
                logger.exception("Failed to enqueue Office completion for %s", task_id)

        except Exception as e:
            logger.error(f"Error executing task {task_id}: {e}")
            self._fail_task(task_id, str(e))
        finally:
            heartbeat.cancel()
            try:
                await heartbeat
            except asyncio.CancelledError:
                pass

    async def _heartbeat_claim(self, task_id: str) -> None:
        try:
            while True:
                await asyncio.sleep(self.heartbeat_interval)
                with _supervisor_db_lock:
                    self.db._execute_write(
                        lambda conn: conn.execute(
                            "UPDATE delegate_tasks SET updated_at = ? "
                            "WHERE id = ? AND status = 'working'",
                            (time.time(), task_id),
                        )
                    )
        except asyncio.CancelledError:
            return

    def _recover_stale_claims(self) -> int:
        cutoff = time.time() - self.claim_timeout

        def _recover(conn):
            cursor = conn.execute(
                "UPDATE delegate_tasks SET status = 'queued', updated_at = ? "
                "WHERE status = 'working' AND updated_at < ?",
                (time.time(), cutoff),
            )
            conn.execute(
                "UPDATE workers SET status = 'idle' WHERE status = 'working' "
                "AND archived_at IS NULL AND NOT EXISTS ("
                "SELECT 1 FROM delegate_tasks active WHERE active.worker_id = workers.worker_id "
                "AND active.status = 'working')"
            )
            return cursor.rowcount

        with _supervisor_db_lock:
            recovered = self.db._execute_write(_recover)
        if recovered:
            logger.warning("WorkerSupervisor recovered %d stale task claim(s)", recovered)
        return recovered

    @staticmethod
    def _json_dict(value) -> dict:
        if isinstance(value, dict):
            return dict(value)
        if isinstance(value, str) and value.strip():
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return {}
            return parsed if isinstance(parsed, dict) else {}
        return {}

    def _resolve_worker_runtime(self, parent_session_id: Optional[str]) -> tuple[dict, dict]:
        """Resolve the worker from its owning profile and parent session.

        Persistent office work is executed on the supervisor thread, long after
        the live parent ``AIAgent`` may have disappeared.  Reconstruct the same
        route from durable session metadata, then let the profile-scoped runtime
        resolver obtain fresh credentials/credential pools.  API keys are never
        read from SQLite.
        """
        from pixel_cli.config import load_config_readonly
        from pixel_cli.runtime_provider import (
            canonical_custom_identity,
            format_runtime_provider_error,
            resolve_runtime_provider,
        )

        cfg = load_config_readonly()
        model_cfg = cfg.get("model") if isinstance(cfg, dict) else {}
        if isinstance(model_cfg, str):
            configured_model = model_cfg.strip()
        elif isinstance(model_cfg, dict):
            configured_model = str(
                model_cfg.get("default") or model_cfg.get("model") or ""
            ).strip()
        else:
            configured_model = ""

        parent = self.db.get_session(parent_session_id) if parent_session_id else None
        parent_config = self._json_dict(parent.get("model_config")) if parent else {}
        route_lock = parent_config.get("browser_model_lock")
        if not isinstance(route_lock, dict):
            route_lock = {}

        target_model = str(
            route_lock.get("model")
            or (parent.get("model") if parent else "")
            or configured_model
            or ""
        ).strip()
        requested_provider = str(
            route_lock.get("provider")
            or (parent.get("billing_provider") if parent else "")
            or ""
        ).strip()
        parent_base_url = str(
            (parent.get("billing_base_url") if parent else "") or ""
        ).strip()

        # Named custom providers collapse to provider="custom" in session
        # accounting. Recover the routable custom:<name> identity so the
        # resolver can load that profile's key and credential pool.
        explicit_base_url = None
        if requested_provider.lower() == "custom":
            requested_provider = (
                canonical_custom_identity(
                    base_url=parent_base_url,
                    model=target_model,
                )
                or requested_provider
            )
            explicit_base_url = parent_base_url or None

        try:
            runtime = resolve_runtime_provider(
                requested=requested_provider or None,
                explicit_base_url=explicit_base_url,
                target_model=target_model or None,
            )
        except Exception as exc:
            raise RuntimeError(
                "LLM runtime for the assigned worker could not be resolved: "
                + format_runtime_provider_error(exc)
            ) from exc

        if not target_model:
            target_model = str(runtime.get("model") or "").strip()
        if not target_model:
            raise RuntimeError(
                "LLM runtime for the assigned worker has no model. Configure "
                "model.default in this profile before retrying the task."
            )

        runtime["model"] = target_model
        return runtime, cfg if isinstance(cfg, dict) else {}

    def _run_agent_sync(
        self,
        worker,
        template,
        task_id,
        goal,
        deliverable=None,
        acceptance_criteria=None,
        parent_session_id=None,
    ):
        from run_agent import AIAgent
        from agent.secret_scope import (
            build_profile_secret_scope,
            reset_secret_scope,
            set_secret_scope,
        )
        from pixel_constants import (
            reset_pixel_agents_home_override,
            resolve_reasoning_config,
            set_pixel_agents_home_override,
        )
        from pixel_cli.fallback_config import get_fallback_chain

        # ContextVars do not automatically flow into the supervisor's executor
        # thread. Bind both the profile home and its secrets explicitly before
        # config/provider resolution, and always restore the previous context.
        profile_home = Path(self.db.db_path).expanduser().resolve().parent
        home_token = set_pixel_agents_home_override(profile_home)
        secret_token = None
        # Each worker agent gets its OWN SessionDB instance.
        # Previously all workers shared self.db (the supervisor's connection).
        # When supervisor.close() was called (e.g. on atexit or restart), it set
        # self.db._conn = None, causing 'NoneType has no attribute execute' in
        # every agent that was still running. Per-worker DBs are isolated from
        # the supervisor lifecycle and from each other.
        worker_db: Optional[SessionDB] = None
        try:
            secret_token = set_secret_scope(build_profile_secret_scope(profile_home))
            runtime, cfg = self._resolve_worker_runtime(parent_session_id)
            model = runtime["model"]
            delegation_cfg = cfg.get("delegation") or {}
            if not isinstance(delegation_cfg, dict):
                delegation_cfg = {}
            model_cfg = cfg.get("model") or {}
            if not isinstance(model_cfg, dict):
                model_cfg = {}
            max_iterations = delegation_cfg.get("max_iterations", 50)
            try:
                max_iterations = max(1, int(max_iterations))
            except (TypeError, ValueError):
                max_iterations = 50

            max_tokens = runtime.get("max_output_tokens")
            if not isinstance(max_tokens, int) or max_tokens <= 0:
                configured_max_tokens = model_cfg.get("max_tokens")
                max_tokens = (
                    configured_max_tokens
                    if isinstance(configured_max_tokens, int)
                    and configured_max_tokens > 0
                    else None
                )

            # Open a dedicated DB connection for this worker so it is completely
            # isolated from self.db (the supervisor's connection) and from sibling
            # workers. The agent writes its session rows through this connection;
            # the supervisor continues to update delegate_tasks/workers through
            # self.db without any cross-connection race.
            worker_db = SessionDB()

            agent = AIAgent(
                session_id=f"office-{worker.worker_id}",
                parent_session_id=parent_session_id,
                session_db=worker_db,
                platform="subagent",
                model=model,
                provider=runtime.get("provider"),
                requested_provider=runtime.get("requested_provider"),
                base_url=runtime.get("base_url"),
                api_key=runtime.get("api_key"),
                api_mode=runtime.get("api_mode"),
                command=runtime.get("command"),
                args=list(runtime.get("args") or []),
                credential_pool=runtime.get("credential_pool"),
                fallback_model=get_fallback_chain(cfg) or None,
                reasoning_config=resolve_reasoning_config(cfg, model),
                request_overrides=dict(runtime.get("request_overrides") or {}),
                max_tokens=max_tokens,
                max_iterations=max_iterations,
                ephemeral_system_prompt=(
                    f"You are {worker.display_name}, a persistent {template.name} in an AI office.\n\n"
                    f"{template.system_prompt}"
                ),
                allowed_tools=list(dict.fromkeys([*template.allowed_tools, "send_worker_message"])),
                skip_memory=False,
                quiet_mode=True,
            )
            agent._session_init_model_config.update(
                {
                    "_office_worker_id": worker.worker_id,
                    "_office_template_id": template.id,
                }
            )

            # Register in active_agents so send_message_tool can find and steer it
            WorkerSupervisor.active_agents[worker.worker_id] = agent

            # Initial message queue processing logic
            history = []
            contract = []
            if deliverable:
                contract.append(f"EXPECTED DELIVERABLE: {deliverable}")
            if acceptance_criteria:
                contract.append(
                    "ACCEPTANCE CRITERIA:\n"
                    + "\n".join(f"- {item}" for item in acceptance_criteria)
                )
            full_goal = (
                f"TASK ID: {task_id}\n\n{goal}\n\n"
                + ("\n\n".join(contract) + "\n\n" if contract else "")
                + "Complete the task and report concrete evidence for the result."
            )

            result = agent.run_conversation(user_message=full_goal, task_id=task_id)
            result["execution"] = {
                "kind": "office_worker",
                "worker_id": worker.worker_id,
                "worker_name": worker.display_name,
                "template_id": template.id,
                "child_session_id": f"office-{worker.worker_id}",
                "provider": getattr(agent, "provider", None),
                "model": getattr(agent, "model", None),
            }
            return result
        finally:
            if secret_token is not None:
                reset_secret_scope(secret_token)
            reset_pixel_agents_home_override(home_token)
            # Close the worker's own DB connection now that the task is done.
            # The supervisor's self.db remains open for its own bookkeeping.
            if worker_db is not None:
                try:
                    worker_db.close()
                except Exception:
                    pass


    def _fail_task(self, task_id, reason):
        parent_session_id = None
        worker_id = None
        goal = ""
        def _fail(conn):
            nonlocal parent_session_id, worker_id, goal
            now = time.time()
            attempt_id = "attempt-" + uuid.uuid4().hex[:8]
            row = conn.execute("SELECT MAX(attempt_number) as max_attempt FROM delegate_task_attempts WHERE task_id = ?", (task_id,)).fetchone()
            attempt_num = (row["max_attempt"] or 0) + 1

            conn.execute(
                "UPDATE delegate_tasks SET status = 'error', updated_at = ? WHERE id = ?",
                (now, task_id)
            )
            conn.execute(
                "INSERT INTO delegate_task_attempts (id, task_id, attempt_number, status, result, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (attempt_id, task_id, attempt_num, 'error', reason, now)
            )
            row = conn.execute("SELECT worker_id, parent_session_id, goal FROM delegate_tasks WHERE id = ?", (task_id,)).fetchone()
            if row:
                worker_id = row["worker_id"]
                parent_session_id = row["parent_session_id"]
                goal = row["goal"] or ""
                if worker_id:
                    conn.execute(
                        "UPDATE workers SET status = 'error' WHERE worker_id = ? AND archived_at IS NULL",
                        (worker_id,),
                    )
        with _supervisor_db_lock:
            self.db._execute_write(_fail)

        try:
            from agent.office_events import enqueue_office_completion

            enqueue_office_completion(
                self.db,
                parent_session_id=parent_session_id,
                task_id=task_id,
                worker_id=worker_id,
                goal=goal,
                status="error",
                error=reason,
            )
        except Exception:
            logger.exception("Failed to enqueue Office failure for %s", task_id)


_service_lock = threading.Lock()
_service_instances: dict[str, tuple[WorkerSupervisor, threading.Thread]] = {}


def ensure_worker_supervisor_started(*, poll_interval: float = 2.0) -> WorkerSupervisor:
    """Start one profile-scoped daemon supervisor for the current process."""
    db = SessionDB()
    service_key = str(db.db_path)
    with _service_lock:
        existing = _service_instances.get(service_key)
        if existing is not None and existing[1].is_alive():
            db.close()
            return existing[0]
        supervisor = WorkerSupervisor(poll_interval=poll_interval, db=db)

        def _run() -> None:
            try:
                asyncio.run(supervisor.start())
            except Exception:
                logger.exception("WorkerSupervisor service crashed")

        thread = threading.Thread(target=_run, name="pixel-worker-supervisor", daemon=True)
        _service_instances[service_key] = (supervisor, thread)
        thread.start()
        return supervisor


def stop_worker_supervisor() -> None:
    with _service_lock:
        instances = list(_service_instances.values())
        _service_instances.clear()
        for supervisor, _thread in instances:
            supervisor.stop()
    for supervisor, thread in instances:
        if thread is not threading.current_thread():
            thread.join(timeout=3.0)
        try:
            supervisor.db.close()
        except Exception:
            pass


atexit.register(stop_worker_supervisor)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    supervisor = WorkerSupervisor()
    try:
        asyncio.run(supervisor.start())
    except KeyboardInterrupt:
        supervisor.stop()
