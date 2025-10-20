from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.utils import success_response
from app.modules.logs.service import LogService
from app.modules.users.controller import get_current_user
from app.modules.users.schemas import UserResponse

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/", response_model=dict)
def get_all_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = LogService(db)
        logs = service.get_all_logs(skip, limit)
        return success_response([log.model_dump() for log in logs], "Logs obtenidos exitosamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/user/{user_id}", response_model=dict)
def get_logs_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = LogService(db)
        logs = service.get_logs_by_user(user_id, skip, limit)
        return success_response([log.model_dump() for log in logs], "Logs del usuario obtenidos exitosamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
