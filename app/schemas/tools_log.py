from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models import ActionType
from .user import User

class ToolsLogBase(BaseModel):
    target_object_id: int
    action: ActionType

class ToolsLogCreate(ToolsLogBase):
    user_id: int
    room_id: int

class ToolsLog(ToolsLogBase):
    id: int
    user_id: int
    room_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ToolsLogWithUser(ToolsLog):
    user: User
    
    class Config:
        from_attributes = True
