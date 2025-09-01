from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import User
from app.schemas import RoomUser, RoomUserWithUser
from app.services.room_service import RoomService
from app.auth import get_current_active_user

router = APIRouter()

room_service = RoomService()

@router.get("/room/{room_id}", 
    response_model=List[RoomUserWithUser],
    summary="방 참여자 목록 조회",
    description="""
특정 방에 참여하고 있는 사용자 목록을 조회합니다.

## 경로 파라미터
- `room_id`: 조회할 방의 ID

## 응답 예시
```json
[
    {
        "id": 1,
        "room_id": 1,
        "user_id": 1,
        "x": 100,
        "y": 200,
        "last_seen": "2024-01-01T00:00:00Z",
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
- 실시간 위치 정보는 WebSocket을 통해 업데이트됩니다
- `last_seen`은 마지막 활동 시간을 나타냅니다
- 방에 참여한 사용자만 조회 가능합니다
""",
    responses={
        200: {
            "description": "방 참여자 목록 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "room_id": 1,
                            "user_id": 1,
                            "x": 100,
                            "y": 200,
                            "last_seen": "2024-01-01T00:00:00Z",
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
async def read_room_users(
    room_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get all users in a specific room"""
    return await room_service.get_room_users(room_id)

@router.post("/room/{room_id}/join", 
    response_model=RoomUserWithUser,
    summary="방 참여",
    description="""
특정 방에 참여합니다.

## 경로 파라미터
- `room_id`: 참여할 방의 ID

## 요청 본문
```json
{
    "x": 100,
    "y": 200
}
```

## 응답 예시
```json
{
    "id": 1,
    "room_id": 1,
    "user_id": 1,
    "x": 100,
    "y": 200,
    "last_seen": "2024-01-01T00:00:00Z",
    "user": {
        "id": 1,
        "username": "john_doe",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

## 실시간 참여
WebSocket을 통해 실시간으로 방에 참여할 수도 있습니다:
```javascript
ws.send(JSON.stringify({
    event: "join_room",
    data: {
        room_id: 1,
        x: 100,
        y: 200
    }
}));
```
""",
    responses={
        200: {
            "description": "방 참여 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "room_id": 1,
                        "user_id": 1,
                        "x": 100,
                        "y": 200,
                        "last_seen": "2024-01-01T00:00:00Z",
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
        },
        409: {
            "description": "이미 방에 참여 중",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User already in room"
                    }
                }
            }
        }
    }
)
async def join_room(
    room_id: int,
    x: int = 0,
    y: int = 0,
    current_user: User = Depends(get_current_active_user)
):
    """Join a room"""
    return await room_service.join_room(current_user.id, room_id, x, y)

@router.post("/room/{room_id}/leave", 
    summary="방 나가기",
    description="""
특정 방에서 나갑니다.

## 경로 파라미터
- `room_id`: 나갈 방의 ID

## 응답 예시
```json
{
    "message": "Successfully left room"
}
```

## 실시간 나가기
WebSocket을 통해 실시간으로 방에서 나갈 수도 있습니다:
```javascript
ws.send(JSON.stringify({
    event: "leave_room",
    data: {
        room_id: 1
    }
}));
```
""",
    responses={
        200: {
            "description": "방 나가기 성공",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Successfully left room"
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
async def leave_room(
    room_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Leave a room"""
    await room_service.leave_room(current_user.id, room_id)
    return {"message": "Successfully left room"}

@router.put("/room/{room_id}/position", 
    response_model=RoomUserWithUser,
    summary="방 내 위치 업데이트",
    description="""
방 내에서의 위치를 업데이트합니다.

## 경로 파라미터
- `room_id`: 위치를 업데이트할 방의 ID

## 요청 본문
```json
{
    "x": 150,
    "y": 250
}
```

## 응답 예시
```json
{
    "id": 1,
    "room_id": 1,
    "user_id": 1,
    "x": 150,
    "y": 250,
    "last_seen": "2024-01-01T00:00:00Z",
    "user": {
        "id": 1,
        "username": "john_doe",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

## 실시간 위치 업데이트
WebSocket을 통해 실시간으로 위치를 업데이트할 수도 있습니다:
```javascript
ws.send(JSON.stringify({
    event: "update_position",
    data: {
        room_id: 1,
        x: 150,
        y: 250
    }
}));
```
""",
    responses={
        200: {
            "description": "위치 업데이트 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "room_id": 1,
                        "user_id": 1,
                        "x": 150,
                        "y": 250,
                        "last_seen": "2024-01-01T00:00:00Z",
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
async def update_position(
    room_id: int,
    x: int,
    y: int,
    current_user: User = Depends(get_current_active_user)
):
    """Update user position in a room"""
    return await room_service.update_user_position(current_user.id, room_id, x, y)
