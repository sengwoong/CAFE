from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import User
from app.schemas import Room, RoomCreate, RoomUpdate, RoomDetail
from app.services.room_service import RoomService
from app.auth import get_current_active_user

router = APIRouter()

room_service = RoomService()

@router.get("/", 
    response_model=List[Room],
    summary="방 목록 조회",
    description="""
모든 방 목록을 조회합니다. 기본적으로 공개 방만 조회합니다.

## 쿼리 파라미터
- `skip`: 건너뛸 항목 수 (기본값: 0)
- `limit`: 조회할 항목 수 (기본값: 100)
- `public_only`: 공개 방만 조회 여부 (기본값: true)

## 응답 예시
```json
[
    {
        "id": 1,
        "name": "커피숍",
        "owner_id": 1,
        "is_private": False,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```
""",
    responses={
        200: {
            "description": "방 목록 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "커피숍",
                            "owner_id": 1,
                            "is_private": False,
                            "created_at": "2024-01-01T00:00:00Z"
                        }
                    ]
                }
            }
        }
    }
)
async def read_rooms(skip: int = 0, limit: int = 100, public_only: bool = True):
    """Get all rooms (public by default)"""
    return await room_service.get_rooms(skip=skip, limit=limit, public_only=public_only)

@router.post("/", 
    response_model=Room,
    summary="새 방 생성",
    description="""
새로운 가상 공간(방)을 생성합니다.

## 요청 예시
```json
{
    "name": "커피숍",
    "is_private": false
}
```

## 응답 예시
```json
{
    "id": 1,
    "name": "커피숍",
    "owner_id": 1,
    "is_private": False,
    "created_at": "2024-01-01T00:00:00Z"
}
```

## 주의사항
- 방 생성자는 자동으로 방장이 됩니다
- 비공개 방은 방장만 접근할 수 있습니다
""",
    responses={
        200: {
            "description": "방 생성 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "커피숍",
                        "owner_id": 1,
                        "is_private": False,
                        "created_at": "2024-01-01T00:00:00Z"
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
        }
    }
)
async def create_new_room(
    room: RoomCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new room"""
    return await room_service.create_room(room, current_user.id)

@router.get("/{room_id}", 
    response_model=Room,
    summary="방 정보 조회",
    description="""
특정 방의 정보를 조회합니다.

## 경로 파라미터
- `room_id`: 조회할 방의 ID

## 응답 예시
```json
{
    "id": 1,
    "name": "커피숍",
    "owner_id": 1,
    "is_private": False,
    "created_at": "2024-01-01T00:00:00Z"
}
```
""",
    responses={
        200: {
            "description": "방 정보 조회 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "커피숍",
                        "owner_id": 1,
                        "is_private": False,
                        "created_at": "2024-01-01T00:00:00Z"
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
async def read_room(room_id: int):
    """Get a specific room by ID"""
    db_room = await room_service.get_room(room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
