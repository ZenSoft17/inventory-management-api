from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.utils import success_response, error_response
from app.core.security import decode_access_token
from app.modules.users.service import UserService
from app.modules.users.schemas import UserCreate, UserUpdate, UserResponse, UserLogin, Token

router = APIRouter(prefix="/users", tags=["Usuarios"])
auth_router = APIRouter(prefix="/auth", tags=["Autenticación"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserResponse:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas"
        )
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    service = UserService(db)
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    return user

@auth_router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        service = UserService(db)
        new_user = service.register_user(user)
        return success_response(new_user.model_dump(), "Usuario registrado exitosamente")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@auth_router.post("/login", response_model=dict)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        service = UserService(db)
        token = service.authenticate_user(login_data)
        return success_response(token.model_dump(), "Inicio de sesión exitoso")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get("/me", response_model=dict)
def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return success_response(current_user.model_dump(), "Usuario obtenido exitosamente")

@router.get("/", response_model=dict)
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = UserService(db)
        users = service.get_all_users(skip, limit)
        return success_response([user.model_dump() for user in users], "Usuarios obtenidos exitosamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get("/{user_id}", response_model=dict)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return success_response(user.model_dump(), "Usuario obtenido exitosamente")

@router.put("/{user_id}", response_model=dict)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = UserService(db)
        updated_user = service.update_user(user_id, user_update, current_user.id)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return success_response(updated_user.model_dump(), "Usuario actualizado exitosamente")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    service = UserService(db)
    deleted = service.delete_user(user_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return success_response(None, "Usuario eliminado exitosamente")
