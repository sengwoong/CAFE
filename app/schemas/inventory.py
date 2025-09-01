from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models import ObjectType


class InventoryItemBase(BaseModel):
    type: ObjectType
    quantity: int = Field(default=1, ge=1)
    metadata: Optional[Dict[str, Any]] = None


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItem(InventoryItemBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class InventoryPlaceRequest(BaseModel):
    inventory_item_id: int
    room_id: int
    x: int
    y: int
    rotation: float = 0.0


