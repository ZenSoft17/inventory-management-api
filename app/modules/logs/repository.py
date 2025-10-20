from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.logs.models import Log
from app.modules.logs.schemas import LogCreate

class LogRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, log: LogCreate) -> Log:
        db_log = Log(**log.model_dump())
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log
    
    def get_by_id(self, log_id: int) -> Optional[Log]:
        return self.db.query(Log).filter(Log.id == log_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Log]:
        return self.db.query(Log).order_by(Log.created.desc()).offset(skip).limit(limit).all()
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Log]:
        return self.db.query(Log).filter(Log.user_id == user_id).order_by(Log.created.desc()).offset(skip).limit(limit).all()
    
    def delete(self, log_id: int) -> bool:
        db_log = self.get_by_id(log_id)
        if not db_log:
            return False
        self.db.delete(db_log)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        return self.db.query(Log).count()
