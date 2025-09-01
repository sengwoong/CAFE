from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import User, ObjectType
from app.schemas import Object, ObjectCreate, ObjectUpdate
from app.services.object_service import ObjectService
from app.auth import get_current_active_user

router = APIRouter()

object_service = ObjectService()

@router.get("/", 
    response_model=List[Object],
    summary="모든 오브젝트 조회",
    description="""
모든 오브젝트 목록을 조회합니다.

## 쿼리 파라미터
- `skip`: 건너뛸 오브젝트 수 (기본값: 0)
- `limit`: 조회할 오브젝트 수 (기본값: 100)
- `type`: 오브젝트 타입 필터 (chair, wall, tool 등)

## 응답 예시
```json
[
    {
        "id": 1,
        "room_id": 1,
        "type": "chair",
        "x": 100,
        "y": 200,
        "rotation": 0.0,
        "metadata": {
            "color": "brown",
            "material": "wood"
        },
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

## 오브젝트 타입
- `chair`: 의자
- `wall`: 벽
- `tool`: 도구
- `table`: 테이블
- `decoration`: 장식품
""",
    responses={
        200: {
            "description": "오브젝트 목록 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "room_id": 1,
                            "type": "chair",
                            "x": 100,
                            "y": 200,
                            "rotation": 0.0,
                            "metadata": {
                                "color": "brown",
                                "material": "wood"
                            },
                            "created_at": "2024-01-01T00:00:00Z"
                        }
                    ]
                }
            }
        }
    }
)
async def read_objects(skip: int = 0, limit: int = 100, type: ObjectType = None):
    """Get all objects"""
    return await object_service.get_objects(skip=skip, limit=limit, type=type)

@router.post("/", 
    response_model=Object,
    summary="새 오브젝트 생성",
    description="""
새로운 오브젝트를 생성합니다.

## 요청 본문
```json
{
    "room_id": 1,
    "type": "chair",
    "x": 100,
    "y": 200,
    "rotation": 0.0,
    "metadata": {
        "color": "brown",
        "material": "wood"
    }
}
```

## 필수 필드
- `room_id`: 오브젝트가 위치할 방의 ID
- `type`: 오브젝트 타입 (chair, wall, tool 등)
- `x`, `y`: 오브젝트의 좌표

## 선택 필드
- `rotation`: 회전 각도 (기본값: 0.0)
- `metadata`: 추가 정보 (JSON 형태)

## 응답 예시
```json
{
    "id": 1,
    "room_id": 1,
    "type": "chair",
    "x": 100,
    "y": 200,
    "rotation": 0.0,
    "metadata": {
        "color": "brown",
        "material": "wood"
    },
    "created_at": "2024-01-01T00:00:00Z"
}
```
""",
    responses={
        200: {
            "description": "오브젝트 생성 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "room_id": 1,
                        "type": "chair",
                        "x": 100,
                        "y": 200,
                        "rotation": 0.0,
                        "metadata": {
                            "color": "brown",
                            "material": "wood"
                        },
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
async def create_object(
    object: ObjectCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new object"""
    return await object_service.create_object(object)

@router.get("/{object_id}", 
    response_model=Object,
    summary="특정 오브젝트 조회",
    description="""
특정 오브젝트의 상세 정보를 조회합니다.

## 경로 파라미터
- `object_id`: 조회할 오브젝트의 ID

## 응답 예시
```json
{
    "id": 1,
    "room_id": 1,
    "type": "chair",
    "x": 100,
    "y": 200,
    "rotation": 0.0,
    "metadata": {
        "color": "brown",
        "material": "wood"
    },
    "created_at": "2024-01-01T00:00:00Z"
}
```
""",
    responses={
        200: {
            "description": "오브젝트 조회 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "room_id": 1,
                        "type": "chair",
                        "x": 100,
                        "y": 200,
                        "rotation": 0.0,
                        "metadata": {
                            "color": "brown",
                            "material": "wood"
                        },
                        "created_at": "2024-01-01T00:00:00Z"
                    }
                }
            }
        },
        404: {
            "description": "오브젝트를 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Object not found"
                    }
                }
            }
        }
    }
)
async def read_object(object_id: int):
    """Get a specific object"""
    return await object_service.get_object(object_id)

@router.get("/room/{room_id}", 
    response_model=List[Object],
    summary="방별 오브젝트 조회",
    description="""
특정 방에 있는 모든 오브젝트를 조회합니다.

## 경로 파라미터
- `room_id`: 조회할 방의 ID

## 쿼리 파라미터
- `skip`: 건너뛸 오브젝트 수 (기본값: 0)
- `limit`: 조회할 오브젝트 수 (기본값: 100)
- `type`: 오브젝트 타입 필터

## 응답 예시
```json
[
    {
        "id": 1,
        "room_id": 1,
        "type": "chair",
        "x": 100,
        "y": 200,
        "rotation": 0.0,
        "metadata": {
            "color": "brown",
            "material": "wood"
        },
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```
""",
    responses={
        200: {
            "description": "방 오브젝트 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "room_id": 1,
                            "type": "chair",
                            "x": 100,
                            "y": 200,
                            "rotation": 0.0,
                            "metadata": {
                                "color": "brown",
                                "material": "wood"
                            },
                            "created_at": "2024-01-01T00:00:00Z"
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
async def read_room_objects(room_id: int, skip: int = 0, limit: int = 100):
    """Get all objects in a specific room"""
    return await object_service.get_room_objects(room_id, skip=skip, limit=limit)

