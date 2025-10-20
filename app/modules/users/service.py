from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import timedelta
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from app.core.security import verify_password, create_access_token
from app.core.config import settings

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register_user(self, user: UserCreate) -> UserResponse:
        existing_user = self.repository.get_by_email(user.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        db_user = self.repository.create(user)
        return UserResponse.model_validate(db_user)
    
    def authenticate_user(self, login_data: UserLogin) -> Token:
        user = self.repository.get_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.password):
            raise ValueError("Incorrect email or password")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.repository.get_by_email(email)
        if not user:
            return None
        return UserResponse.model_validate(user)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_all(skip, limit)
        return [UserResponse.model_validate(user) for user in users]
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserResponse]:
        if user_update.email:
            existing_user = self.repository.get_by_email(user_update.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already in use")
        
        updated_user = self.repository.update(user_id, user_update)
        if not updated_user:
            return None
        return UserResponse.model_validate(updated_user)
    
    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete(user_id)
