from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.logs.repository import LogRepository
from app.modules.logs.schemas import LogCreate, LogResponse

class LogService:
    def __init__(self, db: Session):
        self.repository = LogRepository(db)
    
    def create_log(self, log: LogCreate) -> LogResponse:
        db_log = self.repository.create(log)
        return LogResponse.model_validate(db_log)
    
    def get_log_by_id(self, log_id: int) -> Optional[LogResponse]:
        log = self.repository.get_by_id(log_id)
        if not log:
            return None
        return LogResponse.model_validate(log)
    
    def get_all_logs(self, skip: int = 0, limit: int = 100) -> List[LogResponse]:
        logs = self.repository.get_all(skip, limit)
        return [LogResponse.model_validate(log) for log in logs]
    
    def get_logs_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[LogResponse]:
        logs = self.repository.get_by_user_id(user_id, skip, limit)
        return [LogResponse.model_validate(log) for log in logs]
    
    def delete_log(self, log_id: int) -> bool:
        return self.repository.delete(log_id)
    
    def get_statistics(self) -> dict:
        total = self.repository.count_total()
        return {"total_logs": total}
