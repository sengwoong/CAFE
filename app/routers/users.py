from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import User
from app.schemas import User as UserSchema, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.auth import get_current_active_user

router = APIRouter()

user_service = UserService()

@router.get("/", 
    response_model=List[UserSchema],
    summary="모든 사용자 조회",
    description="""
모든 사용자 목록을 조회합니다.

## 쿼리 파라미터
- `skip`: 건너뛸 사용자 수 (기본값: 0)
- `limit`: 조회할 사용자 수 (기본값: 100)

## 응답 예시
```json
[
    {
        "id": 1,
        "username": "john_doe",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

## 주의사항
- 인증된 사용자만 조회 가능합니다
- 민감한 정보는 제외됩니다
""",
    responses={
        200: {
            "description": "사용자 목록 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "username": "john_doe",
                            "avatar_url": "https://example.com/avatar.jpg",
                            "created_at": "2024-01-01T00:00:00Z"
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
        }
    }
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get all users"""
    return await user_service.get_users(skip=skip, limit=limit)

@router.post("/", response_model=UserSchema)
async def create_new_user(user: UserCreate):
    """Create a new user"""
    return await user_service.create_user(user)

@router.get("/me", 
    response_model=UserSchema,
    summary="현재 사용자 정보 조회",
    description="""
현재 로그인한 사용자의 정보를 조회합니다.

## 응답 예시
```json
{
    "id": 1,
    "username": "john_doe",
    "avatar_url": "https://example.com/avatar.jpg",
    "created_at": "2024-01-01T00:00:00Z"
}
```

## 주의사항
- JWT 토큰이 필요합니다
- 본인의 정보만 조회 가능합니다
""",
    responses={
        200: {
            "description": "현재 사용자 정보 조회 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "john_doe",
                        "avatar_url": "https://example.com/avatar.jpg",
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
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@router.get("/{user_id}", 
    response_model=UserSchema,
    summary="특정 사용자 정보 조회",
    description="""
특정 사용자의 정보를 조회합니다.

## 경로 파라미터
- `user_id`: 조회할 사용자의 ID

## 응답 예시
```json
{
    "id": 1,
    "username": "john_doe",
    "avatar_url": "https://example.com/avatar.jpg",
    "created_at": "2024-01-01T00:00:00Z"
}
```

## 주의사항
- 인증된 사용자만 조회 가능합니다
- 민감한 정보는 제외됩니다
""",
    responses={
        200: {
            "description": "사용자 정보 조회 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "john_doe",
                        "avatar_url": "https://example.com/avatar.jpg",
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
            "description": "사용자를 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found"
                    }
                }
            }
        }
    }
)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific user by ID"""
    db_user = await user_service.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/me", 
    response_model=UserSchema,
    summary="현재 사용자 정보 수정",
    description="""
현재 로그인한 사용자의 정보를 수정합니다.

## 요청 본문
```json
{
    "username": "new_username",
    "avatar_url": "https://example.com/new_avatar.jpg"
}
```

## 수정 가능한 필드
- `username`: 사용자명
- `avatar_url`: 아바타 이미지 URL

## 응답 예시
```json
{
    "id": 1,
    "username": "new_username",
    "avatar_url": "https://example.com/new_avatar.jpg",
    "created_at": "2024-01-01T00:00:00Z"
}
```

## 주의사항
- 본인의 정보만 수정 가능합니다
- 사용자명은 중복될 수 없습니다
""",
    responses={
        200: {
            "description": "사용자 정보 수정 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "new_username",
                        "avatar_url": "https://example.com/new_avatar.jpg",
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
        400: {
            "description": "잘못된 요청",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Username already exists"
                    }
                }
            }
        }
    }
)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user information"""
    return await user_service.update_user(current_user.id, user_update)

@router.delete("/me", 
    summary="현재 사용자 계정 삭제",
    description="""
현재 로그인한 사용자의 계정을 삭제합니다.

## 응답 예시
```json
{
    "message": "User deleted successfully"
}
```

## 주의사항
- 본인의 계정만 삭제 가능합니다
- 삭제된 계정은 복구할 수 없습니다
- 관련된 모든 데이터가 함께 삭제됩니다
""",
    responses={
        200: {
            "description": "사용자 계정 삭제 성공",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User deleted successfully"
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
async def delete_user_me(current_user: User = Depends(get_current_active_user)):
    """Delete current user account"""
    await user_service.delete_user(current_user.id)
    return {"message": "User deleted successfully"}
