from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.logs.repository import LogRepository
from app.modules.logs.schemas import LogCreate, LogResponse

class LogService:
    def __init__(self, db: Session):
        self.repository = LogRepository(db)
    
    def create_log(self, user_id: int, action: str) -> None:
        log = LogCreate(user_id=user_id, action=action)
        self.repository.create(log)
    
    def get_all_logs(self, skip: int = 0, limit: int = 100) -> List[LogResponse]:
        logs = self.repository.get_all(skip, limit)
        return [LogResponse.model_validate(log) for log in logs]
    
    def get_logs_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[LogResponse]:
        logs = self.repository.get_by_user_id(user_id, skip, limit)
        return [LogResponse.model_validate(log) for log in logs]
