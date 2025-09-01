from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.database import engine
from app.models import Base
from app.routers import (
    auth_router, users_router, rooms_router, objects_router,
    chat_router, tools_router, room_users_router, websocket_router
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cafe Virtual Space API",
    description="""
# 🏪 Cafe Virtual Space API

가상 카페 공간을 위한 실시간 WebSocket 기반 API입니다.

## 🌟 주요 기능

### 🔐 인증 (Authentication)
- JWT 기반 사용자 인증
- 사용자 등록 및 로그인

### 👥 사용자 관리 (Users)
- 사용자 프로필 관리
- 아바타 설정

### 🏢 방 관리 (Rooms)
- 가상 공간 생성 및 관리
- 공개/비공개 방 설정

### 🪑 오브젝트 관리 (Objects)
- 방 내 오브젝트 (의자, 벽, 도구) 관리
- 위치 및 회전 설정

### 💬 실시간 채팅 (Chat)
- WebSocket 기반 실시간 메시징
- 방별 채팅 로그

### 🛠️ 도구 사용 (Tools)
- 오브젝트 조작 로그
- 사용자 행동 추적

### 🌐 WebSocket 실시간 통신
- 실시간 사용자 위치 업데이트
- 실시간 채팅
- 실시간 도구 사용

## 🔌 WebSocket 이벤트

### 클라이언트 → 서버
- `join_room`: 방 입장
- `leave_room`: 방 퇴장  
- `update_position`: 위치 업데이트
- `send_message`: 메시지 전송
- `use_tool`: 도구 사용

### 서버 → 클라이언트
- `user_joined`: 사용자 입장 알림
- `user_left`: 사용자 퇴장 알림
- `position_updated`: 위치 업데이트 알림
- `message_received`: 메시지 수신
- `tool_used`: 도구 사용 알림

## 🚀 시작하기

1. **환경 설정**
   ```bash
   cp env_example.txt .env
   # .env 파일을 편집하여 데이터베이스 설정
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **서버 실행**
   ```bash
   python run.py
   ```

4. **API 문서 확인**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔗 WebSocket 연결

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws?token=YOUR_JWT_TOKEN');

ws.onopen = () => {
    console.log('WebSocket 연결됨');
    
    // 방 입장
    ws.send(JSON.stringify({
        event: "join_room",
        data: { room_id: 1, x: 100, y: 200 }
    }));
};

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log('수신:', message);
};
```

## 📊 데이터베이스 스키마

### Users (사용자)
- `id`: 고유 ID
- `username`: 사용자명
- `avatar_url`: 아바타 URL
- `created_at`: 생성 시간

### Rooms (방)
- `id`: 방 ID
- `name`: 방 이름
- `owner_id`: 방장 ID
- `is_private`: 비공개 여부
- `created_at`: 생성 시간

### Objects (오브젝트)
- `id`: 오브젝트 ID
- `room_id`: 소속 방 ID
- `type`: 타입 (chair, wall, tool)
- `x`, `y`: 위치 좌표
- `rotation`: 회전 각도
- `metadata`: 추가 정보 (JSON)

### RoomUsers (방 사용자)
- `id`: 고유 ID
- `room_id`: 방 ID
- `user_id`: 사용자 ID
- `x`, `y`: 현재 위치
- `last_seen`: 마지막 활동 시간

### ChatLogs (채팅 로그)
- `id`: 로그 ID
- `room_id`: 방 ID
- `user_id`: 사용자 ID
- `message`: 메시지 내용
- `created_at`: 전송 시간

### ToolsLog (도구 사용 로그)
- `id`: 로그 ID
- `user_id`: 사용자 ID
- `room_id`: 방 ID
- `target_object_id`: 대상 오브젝트 ID
- `action`: 행동 (destroy, move)
- `created_at`: 사용 시간

## 🔧 환경 변수

```env
# 데이터베이스 설정
DATABASE_URL=postgresql://username:password@localhost:5432/cafe_db

# Redis 설정 (캐싱용)
REDIS_URL=redis://localhost:6379

# JWT 설정
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 서버 설정
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 📝 라이선스

MIT License
    """,
    version="2.0.0",
    contact={
        "name": "Cafe Virtual Space API",
        "email": "support@cafevirtual.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "개발 서버"
        },
        {
            "url": "https://api.cafevirtual.com",
            "description": "프로덕션 서버"
        }
    ],
    tags=[
        {
            "name": "authentication",
            "description": "사용자 인증 관련 API"
        },
        {
            "name": "users", 
            "description": "사용자 관리 API"
        },
        {
            "name": "rooms",
            "description": "방 관리 API"
        },
        {
            "name": "objects",
            "description": "오브젝트 관리 API"
        },
        {
            "name": "chat",
            "description": "채팅 API"
        },
        {
            "name": "tools",
            "description": "도구 사용 API"
        },
        {
            "name": "room-users",
            "description": "방 사용자 관리 API"
        },
        {
            "name": "websocket",
            "description": "WebSocket 실시간 통신"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(rooms_router, prefix="/api/v1/rooms", tags=["rooms"])
app.include_router(objects_router, prefix="/api/v1/objects", tags=["objects"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(tools_router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(room_users_router, prefix="/api/v1/room-users", tags=["room-users"])
app.include_router(websocket_router, prefix="/api/v1", tags=["websocket"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # WebSocket 경로에 대한 설명 추가
    openapi_schema["paths"]["/api/v1/ws"] = {
        "get": {
            "tags": ["websocket"],
            "summary": "WebSocket 연결",
            "description": """
WebSocket을 통한 실시간 통신을 위한 엔드포인트입니다.

## 연결 방법
```
ws://localhost:8000/api/v1/ws?token=YOUR_JWT_TOKEN
```

## 이벤트 예시

### 방 입장
```json
{
    "event": "join_room",
    "data": {
        "room_id": 1,
        "x": 100,
        "y": 200
    }
}
```

### 위치 업데이트
```json
{
    "event": "update_position",
    "data": {
        "room_id": 1,
        "x": 150,
        "y": 250
    }
}
```

### 메시지 전송
```json
{
    "event": "send_message",
    "data": {
        "room_id": 1,
        "message": "안녕하세요!"
    }
}
```

### 도구 사용
```json
{
    "event": "use_tool",
    "data": {
        "room_id": 1,
        "target_object_id": 5,
        "action": "move"
    }
}
```
            """,
            "parameters": [
                {
                    "name": "token",
                    "in": "query",
                    "required": True,
                    "schema": {
                        "type": "string"
                    },
                    "description": "JWT 인증 토큰"
                }
            ],
            "responses": {
                "101": {
                    "description": "WebSocket 연결 성공",
                    "content": {
                        "application/json": {
                            "example": {
                                "message": "WebSocket 연결됨"
                            }
                        }
                    }
                },
                "4001": {
                    "description": "인증 실패",
                    "content": {
                        "application/json": {
                            "example": {
                                "error": "Invalid token"
                            }
                        }
                    }
                }
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cafe Virtual Space API with WebSocket Support",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "websocket": "/api/v1/ws?token=YOUR_TOKEN",
        "features": [
            "Real-time WebSocket communication",
            "User authentication with JWT",
            "Room management",
            "Object placement and interaction",
            "Live chat system",
            "Tool usage tracking"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "2.0.0",
        "services": {
            "database": "connected",
            "websocket": "ready",
            "authentication": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
