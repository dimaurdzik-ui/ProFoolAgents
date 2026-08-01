import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class WorkerInstance:
    worker_id: str
    template_id: str
    display_name: str
    status: str
    autonomy_mode: str
    manager_id: Optional[str]
    created_at: float
    archived_at: Optional[float]

@dataclasses.dataclass
class DelegateTask:
    id: str
    parent_session_id: str
    worker_role: str
    goal: str
    status: str
    handoff_mode: str
    created_at: float
    updated_at: float
    worker_id: Optional[str] = None
    deliverable: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    deadline: Optional[float] = None
    priority: int = 0
