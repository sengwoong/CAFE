from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum
import json

class ObjectType(enum.Enum):
    CHAIR = "chair"
    WALL = "wall"
    TOOL = "tool"

class ActionType(enum.Enum):
    DESTROY = "destroy"
    MOVE = "move"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    avatar_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    rooms = relationship("Room", back_populates="owner")
    room_users = relationship("RoomUser", back_populates="user")
    chat_logs = relationship("ChatLog", back_populates="user")
    tools_logs = relationship("ToolsLog", back_populates="user")

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="rooms")
    objects = relationship("Object", back_populates="room")
    room_users = relationship("RoomUser", back_populates="room")
    chat_logs = relationship("ChatLog", back_populates="room")
    tools_logs = relationship("ToolsLog", back_populates="room")

class Object(Base):
    __tablename__ = "objects"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    type = Column(Enum(ObjectType), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    rotation = Column(Float, default=0.0)
    metadata = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    room = relationship("Room", back_populates="objects")
    tools_logs = relationship("ToolsLog", back_populates="target_object")
    
    def get_metadata(self):
        if self.metadata:
            return json.loads(self.metadata)
        return {}
    
    def set_metadata(self, data):
        self.metadata = json.dumps(data)

class RoomUser(Base):
    __tablename__ = "room_users"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    room = relationship("Room", back_populates="room_users")
    user = relationship("User", back_populates="room_users")

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    room = relationship("Room", back_populates="chat_logs")
    user = relationship("User", back_populates="chat_logs")

class ToolsLog(Base):
    __tablename__ = "tools_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    target_object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    action = Column(Enum(ActionType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="tools_logs")
    room = relationship("Room", back_populates="tools_logs")
    target_object = relationship("Object", back_populates="tools_logs")
