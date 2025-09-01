from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.auth import get_current_active_user
from app.models import User
from app.schemas.inventory import InventoryItem, InventoryItemCreate, InventoryItem as InventoryItemSchema, InventoryPlaceRequest
from app.services.inventory_service import InventoryService
import json


router = APIRouter()
service = InventoryService()


def _to_schema(item) -> dict:
    return {
        "id": item.id,
        "user_id": item.user_id,
        "type": item.type,
        "quantity": item.quantity,
        "metadata": json.loads(item.meta_json) if getattr(item, "meta_json", None) else None,
        "created_at": item.created_at,
    }


@router.get("/", response_model=List[InventoryItemSchema], summary="사용자 인벤토리 목록")
async def list_inventory(current_user: User = Depends(get_current_active_user)):
    items = await service.list_items(current_user.id)
    return [_to_schema(i) for i in items]


@router.post("/", response_model=InventoryItemSchema, summary="인벤토리 아이템 추가")
async def add_inventory_item(
    payload: InventoryItemCreate,
    current_user: User = Depends(get_current_active_user)
):
    item = await service.add_item(current_user.id, payload.type, payload.quantity, payload.metadata)
    return _to_schema(item)


@router.post("/place", summary="인벤토리 아이템 배치")
async def place_from_inventory(
    payload: InventoryPlaceRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        obj = await service.place_item_from_inventory(
            user_id=current_user.id,
            inventory_item_id=payload.inventory_item_id,
            room_id=payload.room_id,
            x=payload.x,
            y=payload.y,
            rotation=payload.rotation,
        )
        return {"status": "ok", "object_id": obj.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


