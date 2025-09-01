from .auth import router as auth_router
from .users import router as users_router
from .rooms import router as rooms_router
from .objects import router as objects_router
from .chat import router as chat_router
from .tools import router as tools_router
from .room_users import router as room_users_router
from .websocket import router as websocket_router
from .inventory import router as inventory_router

__all__ = [
    "auth_router",
    "users_router",
    "rooms_router", 
    "objects_router",
    "chat_router",
    "tools_router",
    "room_users_router",
    "websocket_router",
    "inventory_router"
]
