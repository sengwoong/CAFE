from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Object, ObjectType
from app.database import get_db

class ObjectService:
    def __init__(self):
        pass

    async def get_object(self, object_id: int) -> Optional[Object]:
        """Get object by ID"""
        db = next(get_db())
        return db.query(Object).filter(Object.id == object_id).first()

    async def get_room_objects(self, room_id: int) -> List[Object]:
        """Get objects in a room"""
        db = next(get_db())
        return db.query(Object).filter(Object.room_id == room_id).all()

    async def create_object(self, room_id: int, obj_type: ObjectType, x: int, y: int, rotation: float = 0.0, metadata: dict = None) -> Object:
        """Create a new object"""
        db = next(get_db())
        db_object = Object(
            room_id=room_id,
            type=obj_type,
            x=x,
            y=y,
            rotation=rotation
        )
        if metadata:
            db_object.set_metadata(metadata)
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    async def update_object(self, object_id: int, **kwargs) -> Optional[Object]:
        """Update object"""
        db = next(get_db())
        db_object = db.query(Object).filter(Object.id == object_id).first()
        if db_object:
            for key, value in kwargs.items():
                if key == "metadata":
                    db_object.set_metadata(value)
                else:
                    setattr(db_object, key, value)
            db.commit()
            db.refresh(db_object)
        return db_object

    async def delete_object(self, object_id: int) -> bool:
        """Delete object"""
        db = next(get_db())
        db_object = db.query(Object).filter(Object.id == object_id).first()
        if db_object:
            db.delete(db_object)
            db.commit()
            return True
        return False
