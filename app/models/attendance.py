from pydantic import BaseModel
from datetime import datetime

class Attendance(BaseModel):
    user_id: str
    user_name: str
    timestamp: datetime