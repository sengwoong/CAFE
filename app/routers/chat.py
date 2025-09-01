from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import User
from app.schemas import ChatLog, ChatLogWithUser
from app.services.chat_service import ChatService
from app.auth import get_current_active_user

router = APIRouter()

chat_service = ChatService()

@router.get("/room/{room_id}", 
    response_model=List[ChatLogWithUser],
    summary="방 채팅 로그 조회",
    description="""
특정 방의 채팅 로그를 조회합니다.

## 경로 파라미터
- `room_id`: 조회할 방의 ID

## 쿼리 파라미터
- `skip`: 건너뛸 메시지 수 (기본값: 0)
- `limit`: 조회할 메시지 수 (기본값: 100)

## 응답 예시
```json
[
    {
        "id": 1,
        "room_id": 1,
        "user_id": 1,
        "message": "안녕하세요!",
        "created_at": "2024-01-01T00:00:00Z",
        "user": {
            "id": 1,
            "username": "john_doe",
            "avatar_url": "https://example.com/avatar.jpg",
            "created_at": "2024-01-01T00:00:00Z"
        }
    }
]
```

## 주의사항
- 최신 메시지부터 조회됩니다
- WebSocket을 통한 실시간 채팅도 지원합니다
""",
    responses={
        200: {
            "description": "채팅 로그 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "room_id": 1,
                            "user_id": 1,
                            "message": "안녕하세요!",
                            "created_at": "2024-01-01T00:00:00Z",
                            "user": {
                                "id": 1,
                                "username": "john_doe",
                                "avatar_url": "https://example.com/avatar.jpg",
                                "created_at": "2024-01-01T00:00:00Z"
                            }
                        }
                    ]
                }
            }
        },
        404: {
            "description": "방을 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Room not found"
                    }
                }
            }
        }
    }
)
async def read_room_chat_logs(room_id: int, skip: int = 0, limit: int = 100):
    """Get chat logs for a specific room"""
    return await chat_service.get_room_messages(room_id, skip=skip, limit=limit)

@router.post("/room/{room_id}", 
    response_model=ChatLogWithUser,
    summary="방에 메시지 전송",
    description="""
특정 방에 메시지를 전송합니다.

## 경로 파라미터
- `room_id`: 메시지를 전송할 방의 ID

## 요청 본문
```json
{
    "message": "안녕하세요!"
}
```

## 응답 예시
```json
{
    "id": 1,
    "room_id": 1,
    "user_id": 1,
    "message": "안녕하세요!",
    "created_at": "2024-01-01T00:00:00Z",
    "user": {
        "id": 1,
        "username": "john_doe",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

## 실시간 채팅
WebSocket을 통해 실시간으로 메시지를 주고받을 수도 있습니다:
```javascript
ws.send(JSON.stringify({
    event: "send_message",
    data: {
        room_id: 1,
        message: "안녕하세요!"
    }
}));
```
""",
    responses={
        200: {
            "description": "메시지 전송 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "room_id": 1,
                        "user_id": 1,
                        "message": "안녕하세요!",
                        "created_at": "2024-01-01T00:00:00Z",
                        "user": {
                            "id": 1,
                            "username": "john_doe",
                            "avatar_url": "https://example.com/avatar.jpg",
                            "created_at": "2024-01-01T00:00:00Z"
                        }
                    }
                }
            }
        },
        401: {
            "description": "인증 필요",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        404: {
            "description": "방을 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Room not found"
                    }
                }
            }
        }
    }
)
async def send_message(
    room_id: int,
    message: str,
    current_user: User = Depends(get_current_active_user)
):
    """Send a message to a room"""
    return await chat_service.send_message(current_user.id, room_id, message)
