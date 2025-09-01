from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Room, RoomUser
from app.schemas.room import RoomCreate, RoomUpdate
from app.database import get_session

class RoomService:
    def __init__(self):
        pass

    async def get_room(self, room_id: int) -> Optional[Room]:
        """Get room by ID"""
        with get_session() as db:
            return db.query(Room).filter(Room.id == room_id).first()

    async def get_rooms(self, skip: int = 0, limit: int = 100, public_only: bool = True) -> List[Room]:
        """Get all rooms"""
        with get_session() as db:
            query = db.query(Room)
            if public_only:
                query = query.filter(Room.is_private == False)
            return query.offset(skip).limit(limit).all()

    async def create_room(self, room: RoomCreate, owner_id: int) -> Room:
        """Create a new room"""
        with get_session() as db:
            db_room = Room(
                name=room.name,
                owner_id=owner_id,
                is_private=room.is_private
            )
            db.add(db_room)
            db.commit()
            db.refresh(db_room)
            return db_room

    async def join_room(self, user_id: int, room_id: int, x: int = 0, y: int = 0) -> RoomUser:
        """Join a room"""
        with get_session() as db:
            # Ensure user is in only one room at a time
            db.query(RoomUser).filter(RoomUser.user_id == user_id).delete()
            room_user = RoomUser(
                room_id=room_id,
                user_id=user_id,
                x=x,
                y=y
            )
            db.add(room_user)
            db.commit()
            db.refresh(room_user)
            return room_user

    async def leave_room(self, user_id: int, room_id: int) -> bool:
        """Leave a room"""
        with get_session() as db:
            room_user = db.query(RoomUser).filter(
                RoomUser.room_id == room_id,
                RoomUser.user_id == user_id
            ).first()
            if room_user:
                db.delete(room_user)
                db.commit()
                return True
            return False

    async def update_user_position(self, user_id: int, room_id: int, x: int, y: int) -> Optional[RoomUser]:
        """Update user position in room"""
        with get_session() as db:
            room_user = db.query(RoomUser).filter(
                RoomUser.room_id == room_id,
                RoomUser.user_id == user_id
            ).first()
            if room_user:
                room_user.x = x
                room_user.y = y
                db.commit()
                db.refresh(room_user)
            return room_user
