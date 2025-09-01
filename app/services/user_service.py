from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.database import get_session

class UserService:
    def __init__(self):
        pass

    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        with get_session() as db:
            return db.query(User).filter(User.id == user_id).first()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        with get_session() as db:
            return db.query(User).filter(User.username == username).first()

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users"""
        with get_session() as db:
            return db.query(User).offset(skip).limit(limit).all()

    async def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        with get_session() as db:
            db_user = User(
                username=user.username,
                avatar_url=user.avatar_url
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user"""
        with get_session() as db:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user:
                update_data = user_update.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(db_user, field, value)
                db.commit()
                db.refresh(db_user)
            return db_user

    async def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        with get_session() as db:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user:
                db.delete(db_user)
                db.commit()
                return True
            return False
