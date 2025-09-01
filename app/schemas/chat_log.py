from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .user import User

class ChatLogBase(BaseModel):
    message: str = Field(..., min_length=1)

class ChatLogCreate(ChatLogBase):
    room_id: int
    user_id: int

class ChatLog(ChatLogBase):
    id: int
    room_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatLogWithUser(ChatLog):
    user: User
    
    class Config:
        from_attributes = True
