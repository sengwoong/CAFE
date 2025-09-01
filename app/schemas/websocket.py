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
    # WebRTC signaling
    RTC_JOIN = "rtc_join"
    RTC_LEAVE = "rtc_leave"
    RTC_OFFER = "rtc_offer"
    RTC_ANSWER = "rtc_answer"
    RTC_ICE_CANDIDATE = "rtc_ice_candidate"
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

class RtcJoinData(BaseModel):
    """RTC join data"""
    room_id: int

class RtcLeaveData(BaseModel):
    """RTC leave data"""
    room_id: int

class RtcOfferData(BaseModel):
    """RTC offer data"""
    room_id: int
    to_user_id: int
    sdp: str

class RtcAnswerData(BaseModel):
    """RTC answer data"""
    room_id: int
    to_user_id: int
    sdp: str

class RtcIceCandidateData(BaseModel):
    """RTC ICE candidate data"""
    room_id: int
    to_user_id: int
    candidate: Dict[str, Any]

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
