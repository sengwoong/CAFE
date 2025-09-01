from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
import json

class ObjectType(enum.Enum):
    CHAIR = "chair"
    WALL = "wall"
    TOOL = "tool"

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
