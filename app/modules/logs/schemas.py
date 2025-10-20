from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LogBase(BaseModel):
    user_id: int
    action: str = Field(..., min_length=1, max_length=500)

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    id: int
    created: datetime
    updated: Optional[datetime] = None
    
    class Config:
        from_attributes = True
