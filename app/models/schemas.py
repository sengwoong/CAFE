from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from models import ObjectType, ActionType

# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    avatar_url: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Room Schemas
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

# Object Schemas
class ObjectBase(BaseModel):
    type: ObjectType
    x: int
    y: int
    rotation: float = 0.0
    metadata: Optional[Dict[str, Any]] = None

class ObjectCreate(ObjectBase):
    room_id: int

class ObjectUpdate(BaseModel):
    type: Optional[ObjectType] = None
    x: Optional[int] = None
    y: Optional[int] = None
    rotation: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class Object(ObjectBase):
    id: int
    room_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# RoomUser Schemas
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

# ChatLog Schemas
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

# ToolsLog Schemas
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

# Response Schemas
class RoomDetail(RoomWithOwner):
    objects: List[Object]
    room_users: List[RoomUserWithUser]
    chat_logs: List[ChatLogWithUser]
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
