from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.utils import success_response, error_response
from app.modules.logs.service import LogService
from app.modules.logs.schemas import LogCreate, LogResponse
from app.modules.users.controller import get_current_user
from app.modules.users.schemas import UserResponse

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_log(
    log: LogCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = LogService(db)
        new_log = service.create_log(log)
        return success_response(new_log.model_dump(), "Registro creado correctamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

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
        return success_response([log.model_dump() for log in logs], "Registros obtenidos correctamente")
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
        return success_response([log.model_dump() for log in logs], "Registros del usuario obtenidos correctamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/statistics", response_model=dict)
def get_statistics(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = LogService(db)
        stats = service.get_statistics()
        return success_response(stats, "Estadisticas obtenidas correctamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{log_id}", response_model=dict)
def get_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    service = LogService(db)
    log = service.get_log_by_id(log_id)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")
    return success_response(log.model_dump(), "Registro obtenido correctamente")

@router.delete("/{log_id}", response_model=dict)
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    service = LogService(db)
    deleted = service.delete_log(log_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")
    return success_response(None, "Registro eliminado correctamente")
