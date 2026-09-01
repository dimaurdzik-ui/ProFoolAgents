import traceback
import sqlite3
from pixel_cli.worker_db import _init_schema, create_task
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
_init_schema(conn)

try:
    print("Testing create_task")
    res = create_task(conn, "task-123", "orchestrator", "test goal")
    print("Task created successfully:", res["id"])
except Exception as e:
    print("Failed!")
    traceback.print_exc()
