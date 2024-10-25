from typing import Optional,Dict
from pydantic import BaseModel

class TaskSchema(BaseModel):
    task_name: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    today_hours: Optional[str] = None
    weekly_hours: Optional[str] = None
    daily_work_track: Optional[Dict[str, Dict[str, str]]]=None

class UpdateTaskSchema(BaseModel):
    task_name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    today_hours: Optional[str] = None
    weekly_hours: Optional[str] = None
    daily_work_track:Optional[Dict[str, Dict[str, str]]]=None
