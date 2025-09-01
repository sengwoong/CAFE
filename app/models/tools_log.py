from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ActionType(enum.Enum):
    DESTROY = "destroy"
    MOVE = "move"

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
