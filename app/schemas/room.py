from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .user import User

class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_private: bool = False

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_private: Optional[bool] = None

class Room(RoomBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoomWithOwner(Room):
    owner: User
    
    class Config:
        from_attributes = True

class RoomDetail(RoomWithOwner):
    objects: List = []
    room_users: List = []
    chat_logs: List = []
    
    class Config:
        from_attributes = True
