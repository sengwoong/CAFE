from typing import List, Optional, Dict, Any
from app.database import get_session
from app.models import InventoryItem, ObjectType, Object


class InventoryService:
    def __init__(self):
        pass

    async def list_items(self, user_id: int) -> List[InventoryItem]:
        with get_session() as db:
            return db.query(InventoryItem).filter(InventoryItem.user_id == user_id).all()

    async def add_item(
        self,
        user_id: int,
        obj_type: ObjectType,
        quantity: int = 1,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> InventoryItem:
        with get_session() as db:
            item = InventoryItem(user_id=user_id, type=obj_type, quantity=quantity)
            if metadata:
                # lazy import to avoid circular
                import json
                item.meta_json = json.dumps(metadata)
            db.add(item)
            db.commit()
            db.refresh(item)
            return item

    async def place_item_from_inventory(
        self,
        user_id: int,
        inventory_item_id: int,
        room_id: int,
        x: int,
        y: int,
        rotation: float = 0.0,
    ) -> Object:
        """Place an inventory item into a room as an Object, decrementing inventory quantity."""
        from app.services.object_service import ObjectService

        with get_session() as db:
            item = db.query(InventoryItem).filter(
                InventoryItem.id == inventory_item_id,
                InventoryItem.user_id == user_id,
            ).first()
            if not item:
                raise ValueError("Inventory item not found")

            metadata = None
            if item.meta_json:
                import json
                metadata = json.loads(item.meta_json)

            object_service = ObjectService()
            created = await object_service.create_object(
                room_id=room_id,
                obj_type=item.type,
                x=x,
                y=y,
                rotation=rotation,
                metadata=metadata,
            )

            # decrement or delete inventory item
            if item.quantity > 1:
                item.quantity -= 1
                db.add(item)
            else:
                db.delete(item)
            db.commit()

            return created


