import sys
import traceback
from pixel_cli.worker_db import connect, create_task

try:
    conn = connect()
    print("Connected")
    res = create_task(conn, "test-task-1", "orchestrator", "test goal")
    print("Task created:", res)
except Exception as e:
    print("Exception:")
    traceback.print_exc()
