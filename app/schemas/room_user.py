from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .user import User

class RoomUserBase(BaseModel):
    x: int
    y: int

class RoomUserCreate(RoomUserBase):
    room_id: int
    user_id: int

class RoomUserUpdate(RoomUserBase):
    pass

class RoomUser(RoomUserBase):
    id: int
    room_id: int
    user_id: int
    last_seen: datetime
    
    class Config:
        from_attributes = True

class RoomUserWithUser(RoomUser):
    user: User
    
    class Config:
        from_attributes = True
