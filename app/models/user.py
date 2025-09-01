from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

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
    inventory_items = relationship("InventoryItem", back_populates="user")
