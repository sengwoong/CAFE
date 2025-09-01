# Cafe Virtual Space API (WebSocket Version)

A FastAPI-based backend for managing virtual spaces, rooms, objects, and user interactions with real-time WebSocket support.

## 🚀 Features

- **Real-time Communication**: WebSocket-based real-time updates
- **User Management**: Register, login, and manage user profiles
- **Room Management**: Create, join, and manage virtual rooms
- **Object System**: Add and manage objects (chairs, walls, tools) in rooms
- **Real-time Position Tracking**: Live user position updates via WebSocket
- **Live Chat System**: Real-time messaging in rooms
- **Tool Usage Logging**: Real-time tool interaction logging
- **Authentication**: JWT-based authentication system

## 📁 Project Structure

```
cafe/
├── app/
│   ├── __init__.py
│   ├── database.py              # Database configuration
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── object.py
│   │   ├── room_user.py
│   │   ├── chat_log.py
│   │   └── tools_log.py
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── object.py
│   │   ├── room_user.py
│   │   ├── chat_log.py
│   │   ├── tools_log.py
│   │   ├── auth.py
│   │   └── websocket.py
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── room_service.py
│   │   ├── object_service.py
│   │   ├── chat_service.py
│   │   ├── tools_service.py
│   │   └── websocket_service.py
│   └── routers/                 # API route modules
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       ├── rooms.py
│       ├── objects.py
│       ├── chat.py
│       ├── tools.py
│       ├── room_users.py
│       └── websocket.py
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── alembic.ini                  # Alembic configuration
├── env_example.txt              # Environment variables example
├── run.py                       # Easy startup script
└── README.md                    # This file
```

## 🔌 WebSocket Events

### Client to Server Events
- `join_room` - Join a virtual room
- `leave_room` - Leave a virtual room
- `update_position` - Update user position
- `send_message` - Send chat message
- `use_tool` - Use a tool on an object

### Server to Client Events
- `user_joined` - User joined the room
- `user_left` - User left the room
- `position_updated` - User position updated
- `message_received` - New chat message
- `tool_used` - Tool was used
- `error` - Error occurred

## 🛠️ Installation

1. **Clone and setup**
   ```bash
   cd cafe
   pip install -r requirements.txt
   ```

2. **Environment setup**
   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

3. **Database setup**
   - Install PostgreSQL
   - Create database
   - Update DATABASE_URL in .env

4. **Run the application**
   ```bash
   python run.py
   # or
   uvicorn main:app --reload
   ```

## 🌐 WebSocket Usage

### Connect to WebSocket
```javascript
// Connect with authentication token
const ws = new WebSocket('ws://localhost:8000/api/v1/ws?token=YOUR_JWT_TOKEN');

ws.onopen = function() {
    console.log('Connected to WebSocket');
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('Received:', message);
};
```

### Join a Room
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

### Update Position
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

### Send Message
```javascript
ws.send(JSON.stringify({
    event: "send_message",
    data: {
        room_id: 1,
        message: "Hello everyone!"
    }
}));
```

### Use Tool
```javascript
ws.send(JSON.stringify({
    event: "use_tool",
    data: {
        room_id: 1,
        target_object_id: 5,
        action: "move"
    }
}));
```

## 📡 API Endpoints

### REST API
- **Authentication**: `/api/v1/auth/`
- **Users**: `/api/v1/users/`
- **Rooms**: `/api/v1/rooms/`
- **Objects**: `/api/v1/objects/`
- **Chat**: `/api/v1/chat/`
- **Tools**: `/api/v1/tools/`
- **Room Users**: `/api/v1/room-users/`

### WebSocket
- **WebSocket**: `/api/v1/ws?token=YOUR_TOKEN`

## 🔧 Environment Variables

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/cafe_db

# Redis Configuration (for caching)
REDIS_URL=redis://localhost:6379

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 📚 API Documentation

Once running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## 🎯 Key Features

### Real-time Updates
- **Live User Positions**: See other users move in real-time
- **Instant Chat**: Messages appear immediately
- **Tool Interactions**: See when tools are used
- **Room Events**: Know when users join/leave

### Scalable Architecture
- **Service Layer**: Business logic separated from routes
- **Model Layer**: Clean database models
- **Schema Layer**: Input/output validation
- **WebSocket Manager**: Efficient connection management

### Production Ready
- **Error Handling**: Comprehensive error management
- **Authentication**: JWT-based security
- **Validation**: Pydantic schema validation
- **Documentation**: Auto-generated API docs

## 🚀 Quick Start Example

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/api/v1/ws?token=your_token_here"
    
    async with websockets.connect(uri) as websocket:
        # Join room
        await websocket.send(json.dumps({
            "event": "join_room",
            "data": {"room_id": 1, "x": 100, "y": 200}
        }))
        
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")

# Run the test
asyncio.run(test_websocket())
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
