import json
import asyncio
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Room, RoomUser, ChatLog, ToolsLog
from app.schemas.websocket import (
    WebSocketMessage, WebSocketEvent, JoinRoomMessage, 
    LeaveRoomMessage, UpdatePositionMessage, SendMessageData,
    UseToolData, UserPositionData, ChatMessageData, ToolUsageData, ErrorData
)
from app.services.user_service import UserService
from app.services.room_service import RoomService
from app.services.chat_service import ChatService
from app.services.tools_service import ToolsService

class ConnectionManager:
    def __init__(self):
        # room_id -> set of WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # WebSocket -> user_id mapping
        self.connection_users: Dict[WebSocket, int] = {}
        # WebSocket -> room_id mapping
        self.connection_rooms: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.connection_users[websocket] = user_id

    def disconnect(self, websocket: WebSocket):
        user_id = self.connection_users.get(websocket)
        room_id = self.connection_rooms.get(websocket)
        
        if room_id and room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
        
        if websocket in self.connection_users:
            del self.connection_users[websocket]
        if websocket in self.connection_rooms:
            del self.connection_rooms[websocket]

    async def join_room(self, websocket: WebSocket, room_id: int):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
        self.connection_rooms[websocket] = room_id

    def leave_room(self, websocket: WebSocket):
        room_id = self.connection_rooms.get(websocket)
        if room_id and room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
        if websocket in self.connection_rooms:
            del self.connection_rooms[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_room(self, message: str, room_id: int, exclude_websocket: Optional[WebSocket] = None):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if connection != exclude_websocket:
                    try:
                        await connection.send_text(message)
                    except:
                        # Remove broken connection
                        self.disconnect(connection)

class WebSocketService:
    def __init__(self):
        self.manager = ConnectionManager()
        self.user_service = UserService()
        self.room_service = RoomService()
        self.chat_service = ChatService()
        self.tools_service = ToolsService()

    async def handle_websocket(self, websocket: WebSocket, token: str):
        """Handle WebSocket connection and messages"""
        try:
            # Validate token and get user
            user = await self._authenticate_user(token)
            if not user:
                await websocket.close(code=4001, reason="Invalid token")
                return

            await self.manager.connect(websocket, user.id)
            
            while True:
                try:
                    # Receive message
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Process message
                    await self._process_message(websocket, user, message)
                    
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    error_message = WebSocketMessage(
                        event=WebSocketEvent.ERROR,
                        data=ErrorData(error="Invalid message format", details=str(e)).dict()
                    )
                    await self.manager.send_personal_message(error_message.json(), websocket)
                    
        except WebSocketDisconnect:
            pass
        finally:
            self.manager.disconnect(websocket)

    async def _authenticate_user(self, token: str) -> Optional[User]:
        """Authenticate user from token"""
        # This would use your existing auth logic
        # For now, we'll use a simple approach
        try:
            # You should implement proper JWT validation here
            # This is a placeholder
            return None
        except:
            return None

    async def _process_message(self, websocket: WebSocket, user: User, message: dict):
        """Process incoming WebSocket message"""
        event = message.get("event")
        data = message.get("data", {})

        if event == WebSocketEvent.JOIN_ROOM:
            await self._handle_join_room(websocket, user, data)
        elif event == WebSocketEvent.LEAVE_ROOM:
            await self._handle_leave_room(websocket, user, data)
        elif event == WebSocketEvent.UPDATE_POSITION:
            await self._handle_update_position(websocket, user, data)
        elif event == WebSocketEvent.SEND_MESSAGE:
            await self._handle_send_message(websocket, user, data)
        elif event == WebSocketEvent.USE_TOOL:
            await self._handle_use_tool(websocket, user, data)
        else:
            error_message = WebSocketMessage(
                event=WebSocketEvent.ERROR,
                data=ErrorData(error="Unknown event type").dict()
            )
            await self.manager.send_personal_message(error_message.json(), websocket)

    async def _handle_join_room(self, websocket: WebSocket, user: User, data: dict):
        """Handle join room event"""
        try:
            join_data = JoinRoomMessage(**data)
            
            # Join room in database
            room_user = await self.room_service.join_room(user.id, join_data.room_id, join_data.x, join_data.y)
            
            # Join WebSocket room
            await self.manager.join_room(websocket, join_data.room_id)
            
            # Broadcast user joined to room
            user_data = UserPositionData(
                user_id=user.id,
                username=user.username,
                avatar_url=user.avatar_url,
                x=join_data.x,
                y=join_data.y
            )
            
            broadcast_message = WebSocketMessage(
                event=WebSocketEvent.USER_JOINED,
                data=user_data.dict()
            )
            
            await self.manager.broadcast_to_room(
                broadcast_message.json(), 
                join_data.room_id, 
                exclude_websocket=websocket
            )
            
        except Exception as e:
            error_message = WebSocketMessage(
                event=WebSocketEvent.ERROR,
                data=ErrorData(error="Failed to join room", details=str(e)).dict()
            )
            await self.manager.send_personal_message(error_message.json(), websocket)

    async def _handle_leave_room(self, websocket: WebSocket, user: User, data: dict):
        """Handle leave room event"""
        try:
            leave_data = LeaveRoomMessage(**data)
            
            # Leave room in database
            await self.room_service.leave_room(user.id, leave_data.room_id)
            
            # Leave WebSocket room
            self.manager.leave_room(websocket)
            
            # Broadcast user left to room
            user_data = UserPositionData(
                user_id=user.id,
                username=user.username,
                avatar_url=user.avatar_url,
                x=0,
                y=0
            )
            
            broadcast_message = WebSocketMessage(
                event=WebSocketEvent.USER_LEFT,
                data=user_data.dict()
            )
            
            await self.manager.broadcast_to_room(
                broadcast_message.json(), 
                leave_data.room_id, 
                exclude_websocket=websocket
            )
            
        except Exception as e:
            error_message = WebSocketMessage(
                event=WebSocketEvent.ERROR,
                data=ErrorData(error="Failed to leave room", details=str(e)).dict()
            )
            await self.manager.send_personal_message(error_message.json(), websocket)

    async def _handle_update_position(self, websocket: WebSocket, user: User, data: dict):
        """Handle update position event"""
        try:
            position_data = UpdatePositionMessage(**data)
            
            # Update position in database
            await self.room_service.update_user_position(user.id, position_data.room_id, position_data.x, position_data.y)
            
            # Broadcast position update to room
            user_data = UserPositionData(
                user_id=user.id,
                username=user.username,
                avatar_url=user.avatar_url,
                x=position_data.x,
                y=position_data.y
            )
            
            broadcast_message = WebSocketMessage(
                event=WebSocketEvent.POSITION_UPDATED,
                data=user_data.dict()
            )
            
            await self.manager.broadcast_to_room(
                broadcast_message.json(), 
                position_data.room_id, 
                exclude_websocket=websocket
            )
            
        except Exception as e:
            error_message = WebSocketMessage(
                event=WebSocketEvent.ERROR,
                data=ErrorData(error="Failed to update position", details=str(e)).dict()
            )
            await self.manager.send_personal_message(error_message.json(), websocket)

    async def _handle_send_message(self, websocket: WebSocket, user: User, data: dict):
        """Handle send message event"""
        try:
            message_data = SendMessageData(**data)
            
            # Save message to database
            chat_log = await self.chat_service.send_message(user.id, message_data.room_id, message_data.message)
            
            # Broadcast message to room
            chat_data = ChatMessageData(
                user_id=user.id,
                username=user.username,
                avatar_url=user.avatar_url,
                message=message_data.message,
                timestamp=chat_log.created_at
            )
            
            broadcast_message = WebSocketMessage(
                event=WebSocketEvent.MESSAGE_RECEIVED,
                data=chat_data.dict()
            )
            
            await self.manager.broadcast_to_room(
                broadcast_message.json(), 
                message_data.room_id
            )
            
        except Exception as e:
            error_message = WebSocketMessage(
                event=WebSocketEvent.ERROR,
                data=ErrorData(error="Failed to send message", details=str(e)).dict()
            )
            await self.manager.send_personal_message(error_message.json(), websocket)

    async def _handle_use_tool(self, websocket: WebSocket, user: User, data: dict):
        """Handle use tool event"""
        try:
            tool_data = UseToolData(**data)
            
            # Log tool usage in database
            tools_log = await self.tools_service.use_tool(user.id, tool_data.room_id, tool_data.target_object_id, tool_data.action)
            
            # Broadcast tool usage to room
            tool_usage_data = ToolUsageData(
                user_id=user.id,
                username=user.username,
                target_object_id=tool_data.target_object_id,
                action=tool_data.action,
                timestamp=tools_log.created_at
            )
            
            broadcast_message = WebSocketMessage(
                event=WebSocketEvent.TOOL_USED,
                data=tool_usage_data.dict()
            )
            
            await self.manager.broadcast_to_room(
                broadcast_message.json(), 
                tool_data.room_id
            )
            
        except Exception as e:
            error_message = WebSocketMessage(
                event=WebSocketEvent.ERROR,
                data=ErrorData(error="Failed to use tool", details=str(e)).dict()
            )
            await self.manager.send_personal_message(error_message.json(), websocket)
