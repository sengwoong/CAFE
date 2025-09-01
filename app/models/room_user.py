from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

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
