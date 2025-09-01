from sqlalchemy.orm import Session
from typing import List
from app.models import ChatLog
from app.database import get_session

class ChatService:
    def __init__(self):
        pass

    async def send_message(self, user_id: int, room_id: int, message: str) -> ChatLog:
        """Send a message"""
        with get_session() as db:
            chat_log = ChatLog(
                room_id=room_id,
                user_id=user_id,
                message=message
            )
            db.add(chat_log)
            db.commit()
            db.refresh(chat_log)
            return chat_log

    async def get_room_messages(self, room_id: int, skip: int = 0, limit: int = 100) -> List[ChatLog]:
        """Get messages for a room"""
        with get_session() as db:
            return db.query(ChatLog).filter(ChatLog.room_id == room_id).order_by(
                ChatLog.created_at.desc()
            ).offset(skip).limit(limit).all()
