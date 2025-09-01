from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services.websocket_service import WebSocketService

router = APIRouter()

websocket_service = WebSocketService()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """WebSocket endpoint for real-time communication"""
    await websocket_service.handle_websocket(websocket, token)
