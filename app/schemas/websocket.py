from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models import ObjectType, ActionType

class WebSocketEvent(BaseModel):
    """WebSocket event types"""
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"
    UPDATE_POSITION = "update_position"
    SEND_MESSAGE = "send_message"
    USE_TOOL = "use_tool"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    POSITION_UPDATED = "position_updated"
    MESSAGE_RECEIVED = "message_received"
    TOOL_USED = "tool_used"
    ERROR = "error"

class WebSocketMessage(BaseModel):
    """Base WebSocket message schema"""
    event: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class JoinRoomMessage(BaseModel):
    """Join room message"""
    room_id: int
    x: int = 0
    y: int = 0

class LeaveRoomMessage(BaseModel):
    """Leave room message"""
    room_id: int

class UpdatePositionMessage(BaseModel):
    """Update position message"""
    room_id: int
    x: int
    y: int

class SendMessageData(BaseModel):
    """Send message data"""
    room_id: int
    message: str

class UseToolData(BaseModel):
    """Use tool data"""
    room_id: int
    target_object_id: int
    action: ActionType

class UserPositionData(BaseModel):
    """User position data"""
    user_id: int
    username: str
    avatar_url: Optional[str]
    x: int
    y: int

class ChatMessageData(BaseModel):
    """Chat message data"""
    user_id: int
    username: str
    avatar_url: Optional[str]
    message: str
    timestamp: datetime

class ToolUsageData(BaseModel):
    """Tool usage data"""
    user_id: int
    username: str
    target_object_id: int
    action: ActionType
    timestamp: datetime

class ErrorData(BaseModel):
    """Error data"""
    error: str
    details: Optional[str] = None
