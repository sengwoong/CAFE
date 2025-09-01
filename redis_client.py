import redis
import json
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class RoomUserCache:
    @staticmethod
    def set_user_position(room_id: int, user_id: int, x: int, y: int):
        """Set user position in room"""
        key = f"room:{room_id}:user:{user_id}"
        data = {
            "x": x,
            "y": y,
            "timestamp": json.dumps({"timestamp": "now"})  # You might want to use actual timestamp
        }
        redis_client.hset(key, mapping=data)
        redis_client.expire(key, 300)  # Expire after 5 minutes
    
    @staticmethod
    def get_user_position(room_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user position in room"""
        key = f"room:{room_id}:user:{user_id}"
        data = redis_client.hgetall(key)
        if data:
            return {
                "x": int(data.get("x", 0)),
                "y": int(data.get("y", 0)),
                "timestamp": data.get("timestamp")
            }
        return None
    
    @staticmethod
    def get_room_users(room_id: int) -> Dict[str, Dict[str, Any]]:
        """Get all users in a room"""
        pattern = f"room:{room_id}:user:*"
        keys = redis_client.keys(pattern)
        users = {}
        for key in keys:
            user_id = key.split(":")[-1]
            data = redis_client.hgetall(key)
            if data:
                users[user_id] = {
                    "x": int(data.get("x", 0)),
                    "y": int(data.get("y", 0)),
                    "timestamp": data.get("timestamp")
                }
        return users
    
    @staticmethod
    def remove_user_from_room(room_id: int, user_id: int):
        """Remove user from room cache"""
        key = f"room:{room_id}:user:{user_id}"
        redis_client.delete(key)
    
    @staticmethod
    def clear_room_cache(room_id: int):
        """Clear all users from a room"""
        pattern = f"room:{room_id}:user:*"
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
