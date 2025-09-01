from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import User
from app.schemas import ToolsLog, ToolsLogWithUser
from app.services.tools_service import ToolsService
from app.auth import get_current_active_user

router = APIRouter()

tools_service = ToolsService()

@router.post("/use", 
    response_model=ToolsLogWithUser,
    summary="도구 사용 로그 기록",
    description="""
도구 사용을 로그로 기록합니다.

## 요청 본문
```json
{
    "room_id": 1,
    "target_object_id": 5,
    "action": "destroy"
}
```

## 액션 타입
- `destroy`: 오브젝트 파괴
- `move`: 오브젝트 이동
- `rotate`: 오브젝트 회전
- `create`: 새 오브젝트 생성
- `modify`: 오브젝트 수정

## 응답 예시
```json
{
    "id": 1,
    "user_id": 1,
    "room_id": 1,
    "target_object_id": 5,
    "action": "destroy",
    "created_at": "2024-01-01T00:00:00Z",
    "user": {
        "id": 1,
        "username": "john_doe",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

## 실시간 도구 사용
WebSocket을 통해 실시간으로 도구 사용을 기록할 수도 있습니다:
```javascript
ws.send(JSON.stringify({
    event: "use_tool",
    data: {
        room_id: 1,
        target_object_id: 5,
        action: "destroy"
    }
}));
```
""",
    responses={
        200: {
            "description": "도구 사용 로그 기록 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "room_id": 1,
                        "target_object_id": 5,
                        "action": "destroy",
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
            "description": "방 또는 오브젝트를 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Room or object not found"
                    }
                }
            }
        }
    }
)
async def use_tool(
    room_id: int,
    target_object_id: int,
    action: str,
    current_user: User = Depends(get_current_active_user)
):
    """Log tool usage"""
    return await tools_service.use_tool(current_user.id, room_id, target_object_id, action)

@router.get("/user/{user_id}", 
    response_model=List[ToolsLogWithUser],
    summary="사용자별 도구 사용 로그 조회",
    description="""
특정 사용자의 도구 사용 로그를 조회합니다.

## 경로 파라미터
- `user_id`: 조회할 사용자의 ID

## 쿼리 파라미터
- `skip`: 건너뛸 로그 수 (기본값: 0)
- `limit`: 조회할 로그 수 (기본값: 100)

## 응답 예시
```json
[
    {
        "id": 1,
        "user_id": 1,
        "room_id": 1,
        "target_object_id": 5,
        "action": "destroy",
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
- 최신 로그부터 조회됩니다
- 본인의 로그만 조회 가능합니다
""",
    responses={
        200: {
            "description": "사용자 도구 사용 로그 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "room_id": 1,
                            "target_object_id": 5,
                            "action": "destroy",
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
        403: {
            "description": "권한 없음",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authorized to view this user's logs"
                    }
                }
            }
        }
    }
)
async def read_user_tools_logs(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get tool usage logs for a specific user"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this user's logs")
    return await tools_service.get_user_tools_logs(user_id, skip=skip, limit=limit)

@router.get("/room/{room_id}", 
    response_model=List[ToolsLogWithUser],
    summary="방별 도구 사용 로그 조회",
    description="""
특정 방의 도구 사용 로그를 조회합니다.

## 경로 파라미터
- `room_id`: 조회할 방의 ID

## 쿼리 파라미터
- `skip`: 건너뛸 로그 수 (기본값: 0)
- `limit`: 조회할 로그 수 (기본값: 100)

## 응답 예시
```json
[
    {
        "id": 1,
        "user_id": 1,
        "room_id": 1,
        "target_object_id": 5,
        "action": "destroy",
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
- 최신 로그부터 조회됩니다
- 방에 참여한 사용자만 조회 가능합니다
""",
    responses={
        200: {
            "description": "방 도구 사용 로그 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "room_id": 1,
                            "target_object_id": 5,
                            "action": "destroy",
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
async def read_room_tools_logs(
    room_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get tool usage logs for a specific room"""
    return await tools_service.get_room_tools_logs(room_id, skip=skip, limit=limit)
