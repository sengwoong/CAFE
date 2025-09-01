from sqlalchemy.orm import Session
from typing import List
from app.models import ToolsLog, ActionType
from app.database import get_session

class ToolsService:
    def __init__(self):
        pass

    async def use_tool(self, user_id: int, room_id: int, target_object_id: int, action: ActionType) -> ToolsLog:
        """Use a tool"""
        with get_session() as db:
            tools_log = ToolsLog(
                user_id=user_id,
                room_id=room_id,
                target_object_id=target_object_id,
                action=action
            )
            db.add(tools_log)
            db.commit()
            db.refresh(tools_log)
            return tools_log

    async def get_user_tools_logs(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ToolsLog]:
        """Get tool logs for a user"""
        with get_session() as db:
            return db.query(ToolsLog).filter(ToolsLog.user_id == user_id).order_by(
                ToolsLog.created_at.desc()
            ).offset(skip).limit(limit).all()

    async def get_room_tools_logs(self, room_id: int, skip: int = 0, limit: int = 100) -> List[ToolsLog]:
        """Get tool logs for a room"""
        with get_session() as db:
            return db.query(ToolsLog).filter(ToolsLog.room_id == room_id).order_by(
                ToolsLog.created_at.desc()
            ).offset(skip).limit(limit).all()
