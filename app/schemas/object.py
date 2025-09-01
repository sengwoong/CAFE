from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models import ObjectType

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
