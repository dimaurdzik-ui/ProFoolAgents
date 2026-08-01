import asyncio
from typing import Optional

from run_agent import AIAgent
from pixel_cli.worker_db import connect, update_task, update_worker, create_task
from pixel_cli.worker_catalog import get_template

class WorkerRunner:
    def __init__(self, db_profile: Optional[str] = None):
        self.db_profile = db_profile

    def spawn(self, worker_id: str, task_id: str) -> asyncio.Task:
        return asyncio.create_task(self._run_worker_task(worker_id, task_id))

    async def _run_worker_task(self, worker_id: str, task_id: str):
        conn = connect(self.db_profile)
        
        # Load worker
        worker = conn.execute("SELECT * FROM workers WHERE worker_id = ?", (worker_id,)).fetchone()
        if not worker:
            update_task(conn, task_id, 'error', status='failed', last_error='Worker not found')
            return
            
        # Load template
        template = get_template(worker['template_id'])
        if not template:
            update_task(conn, task_id, 'error', status='failed', last_error='Template not found')
            update_worker(conn, worker_id, status='error')
            return
            
        # Update statuses
        update_worker(conn, worker_id, status='working')
        update_task(conn, task_id, 'status_change', status='working')
        
        task = dict(conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone())
        
        system_prompt = template.system_prompt
        
        user_message = f"Goal: {task['goal']}"
        if task.get('deliverable'):
            user_message += f"\nDeliverable: {task['deliverable']}"
        if task.get('acceptance_criteria'):
            user_message += f"\nAcceptance Criteria: {task['acceptance_criteria']}"
            
        # Run agent in thread since run_conversation is sync
        agent = AIAgent(
            session_id=f"worker-{worker_id}",
            platform="worker"
        )
        
        try:
            # We use to_thread to avoid blocking the event loop
            result = await asyncio.to_thread(
                agent.run_conversation,
                user_message=user_message,
                system_message=system_prompt,
                task_id=task_id
            )
            
            # Post process
            final_status = 'done' if worker['autonomy_mode'] == 'autonomous' else 'waiting_approval'
            
            res_content = "No output"
            if isinstance(result, dict):
                res_content = result.get('final_response', str(result))
            elif isinstance(result, str):
                res_content = result
                
            update_task(conn, task_id, 'result', status=final_status, result=res_content)
            update_worker(conn, worker_id, status='idle')
            
        except Exception as e:
            update_task(conn, task_id, 'error', status='failed', last_error=str(e))
            update_worker(conn, worker_id, status='error')
            
    def reject_and_retry(self, task_id: str, feedback: str) -> asyncio.Task:
        return asyncio.create_task(self._retry_worker_task(task_id, feedback))
        
    async def _retry_worker_task(self, task_id: str, feedback: str):
        conn = connect(self.db_profile)
        task = dict(conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone())
        
        if not task:
            return
            
        worker_id = task['worker_id']
        retry_count = task['retry_count'] + 1
        
        if retry_count > task['max_retries']:
            update_task(conn, task_id, 'status_change', status='failed_permanently')
            return
            
        update_task(conn, task_id, 'status_change', status='working', retry_count=retry_count)
        update_worker(conn, worker_id, status='working')
        
        # We just need to send the feedback as a new message to the existing session
        agent = AIAgent(
            session_id=f"worker-{worker_id}",
            platform="worker"
        )
        
        user_message = f"Your previous work was rejected. Feedback: {feedback}\nPlease fix it and try again."
        
        try:
            result = await asyncio.to_thread(
                agent.run_conversation,
                user_message=user_message,
                task_id=task_id
            )
            
            worker = conn.execute("SELECT * FROM workers WHERE worker_id = ?", (worker_id,)).fetchone()
            final_status = 'done' if worker['autonomy_mode'] == 'autonomous' else 'waiting_approval'
            
            res_content = "No output"
            if isinstance(result, dict):
                res_content = result.get('final_response', str(result))
            elif isinstance(result, str):
                res_content = result
                
            update_task(conn, task_id, 'result', status=final_status, result=res_content)
            update_worker(conn, worker_id, status='idle')
            
        except Exception as e:
            update_task(conn, task_id, 'error', status='failed', last_error=str(e))
            update_worker(conn, worker_id, status='error')
