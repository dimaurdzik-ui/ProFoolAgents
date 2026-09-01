import asyncio
from typing import Optional

from run_agent import AIAgent
from pixel_cli.worker_db import connect, update_task, update_worker, create_task, list_workers
from pixel_cli.worker_catalog import get_template
import json
import time

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
            conn.close()
            return
            
        # Load template
        template = get_template(worker['template_id'])
        if not template:
            update_task(conn, task_id, 'error', status='failed', last_error='Template not found')
            update_worker(conn, worker_id, status='error')
            conn.close()
            return
            
        # Update statuses
        update_worker(conn, worker_id, status='working')
        update_task(conn, task_id, 'status_change', status='working')
        
        task = dict(conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone())
        
        system_prompt = template.system_prompt
        
        # Inject team awareness
        try:
            from pixel_state import SessionDB
            db = SessionDB()
            active_workers = [w for w in db.list_workers() if w.status != 'archived']
            staff_info = "\n<active-team-staff>\n"
            if active_workers:
                staff_info += "Current hired team members:\n"
                for w in active_workers:
                    staff_info += f"- Worker ID: {w.worker_id} | Name: {w.display_name} | Role: {w.template_id} | Status: {w.status}\n"
            else:
                staff_info += "No other workers are currently hired. You are the only one on the team.\n"
                staff_info += "If you need a different role to complete the task, you MUST use the propose_hire_worker tool.\n"
            staff_info += "</active-team-staff>\n"
        except Exception:
            staff_info = "\n<active-team-staff>\nError loading team data.</active-team-staff>\n"
        system_prompt += staff_info
        
        user_message = f"Goal: {task['goal']}"
        if task.get('deliverable'):
            user_message += f"\nDeliverable: {task['deliverable']}"
        if task.get('acceptance_criteria'):
            user_message += f"\nAcceptance Criteria: {task['acceptance_criteria']}"
            

        
        def on_tool_start(*cb_args):
            if worker['autonomy_mode'] != 'manual':
                return
                
            if len(cb_args) == 3:
                _, tool_name, tool_args = cb_args
            elif len(cb_args) == 2:
                tool_name, tool_args = cb_args
            else:
                return None
            
            update_task(
                conn, task_id, 'status_change', 
                status='waiting_tool_approval',
                pending_tool_name=tool_name,
                pending_tool_args=json.dumps(tool_args)
            )
            update_worker(conn, worker_id, status='idle')
            
            # Block until approved or rejected
            start_time = time.time()
            while True:
                if time.time() - start_time > 300: # 5 min timeout
                    update_task(conn, task_id, pending_tool_name=None, pending_tool_args=None, modified_tool_args=None, status='working')
                    update_worker(conn, worker_id, status='working')
                    raise Exception("Tool execution timed out waiting for user approval.")
                    
                time.sleep(1)
                current = conn.execute("SELECT status, modified_tool_args FROM tasks WHERE id = ?", (task_id,)).fetchone()
                status = current['status']
                
                if status == 'working':
                    # Approved
                    modified_args_str = current.get('modified_tool_args')
                    parsed_modified_args = None
                    if modified_args_str:
                        try:
                            parsed_modified_args = json.loads(modified_args_str)
                        except json.JSONDecodeError:
                            pass
                    update_task(conn, task_id, pending_tool_name=None, pending_tool_args=None, modified_tool_args=None)
                    update_worker(conn, worker_id, status='working')
                    return parsed_modified_args
                elif status == 'rejected':
                    # Rejected
                    update_task(conn, task_id, pending_tool_name=None, pending_tool_args=None, modified_tool_args=None, status='working')
                    update_worker(conn, worker_id, status='working')
                    raise Exception("Tool execution rejected by user.")
                    
        # Run agent in thread since run_conversation is sync
        agent = AIAgent(
            session_id=f"worker-{worker_id}",
            platform="worker",
            tool_start_callback=on_tool_start
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
        finally:
            conn.close()
            
    def reject_and_retry(self, task_id: str, feedback: str) -> asyncio.Task:
        return asyncio.create_task(self._retry_worker_task(task_id, feedback))
        
    async def _retry_worker_task(self, task_id: str, feedback: str):
        conn = connect(self.db_profile)
        task = dict(conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone())
        
        if not task:
            conn.close()
            return
            
        worker_id = task['worker_id']
        retry_count = task['retry_count'] + 1
        
        if retry_count > task['max_retries']:
            update_task(conn, task_id, 'status_change', status='failed_permanently')
            conn.close()
            return
            
        update_task(conn, task_id, 'status_change', status='working', retry_count=retry_count)
        update_worker(conn, worker_id, status='working')
        
        def on_tool_start_retry(*cb_args):
            if worker['autonomy_mode'] != 'manual':
                return
                
            if len(cb_args) == 3:
                _, tool_name, tool_args = cb_args
            elif len(cb_args) == 2:
                tool_name, tool_args = cb_args
            else:
                return None
            
            update_task(
                conn, task_id, 'status_change', 
                status='waiting_tool_approval',
                pending_tool_name=tool_name,
                pending_tool_args=json.dumps(tool_args)
            )
            update_worker(conn, worker_id, status='idle')
            
            start_time = time.time()
            while True:
                if time.time() - start_time > 300: # 5 min timeout
                    update_task(conn, task_id, pending_tool_name=None, pending_tool_args=None, modified_tool_args=None, status='working')
                    update_worker(conn, worker_id, status='working')
                    raise Exception("Tool execution timed out waiting for user approval.")
                    
                time.sleep(1)
                current = conn.execute("SELECT status, modified_tool_args FROM tasks WHERE id = ?", (task_id,)).fetchone()
                status = current['status']
                
                if status == 'working':
                    modified_args_str = current.get('modified_tool_args')
                    parsed_modified_args = None
                    if modified_args_str:
                        try:
                            parsed_modified_args = json.loads(modified_args_str)
                        except json.JSONDecodeError:
                            pass
                    update_task(conn, task_id, pending_tool_name=None, pending_tool_args=None, modified_tool_args=None)
                    update_worker(conn, worker_id, status='working')
                    return parsed_modified_args
                elif status == 'rejected':
                    update_task(conn, task_id, pending_tool_name=None, pending_tool_args=None, modified_tool_args=None, status='working')
                    update_worker(conn, worker_id, status='working')
                    raise Exception("Tool execution rejected by user.")
        
        # We just need to send the feedback as a new message to the existing session
        agent = AIAgent(
            session_id=f"worker-{worker_id}",
            platform="worker",
            tool_start_callback=on_tool_start_retry
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
        finally:
            conn.close()
