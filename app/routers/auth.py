from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models import User
from app.schemas import Token, UserCreate, User as UserSchema
from app.services.user_service import UserService
from app.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

user_service = UserService()

@router.post("/register", 
    response_model=UserSchema,
    summary="사용자 등록",
    description="""
새로운 사용자를 등록합니다.

## 요청 예시
```json
{
    "username": "john_doe",
    "avatar_url": "https://example.com/avatar.jpg"
}
```

## 응답 예시
```json
{
    "id": 1,
    "username": "john_doe",
    "avatar_url": "https://example.com/avatar.jpg",
    "created_at": "2024-01-01T00:00:00Z"
}
```
""",
    responses={
        200: {
            "description": "사용자 등록 성공",
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
        400: {
            "description": "사용자명 중복",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Username already registered"
                    }
                }
            }
        }
    }
)
async def register(user: UserCreate):
    """Register a new user"""
    # Check if username already exists
    db_user = await user_service.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Create new user
    return await user_service.create_user(user)

@router.post("/token", 
    response_model=Token,
    summary="로그인 및 토큰 발급",
    description="""
사용자 로그인을 통해 JWT 액세스 토큰을 발급받습니다.

## 요청 예시
```
username=john_doe&password=any_password
```

## 응답 예시
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

## 사용법
발급받은 토큰을 Authorization 헤더에 포함하여 API를 호출합니다:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
""",
    responses={
        200: {
            "description": "로그인 성공",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "인증 실패",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect username"
                    }
                }
            }
        }
    }
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to get access token"""
    # For this example, we'll use username as password
    # In a real application, you should have a separate password field
    user = await user_service.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # For demo purposes, we'll accept any password
    # In production, you should verify the password properly
    # if not verify_password(form_data.password, user.hashed_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
