from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
import json

class ObjectType(enum.Enum):
    CHAIR = "chair"
    TABLE = "table"
    DESK = "desk"
    PLANT = "plant"
    BALLOON = "balloon"
    POT = "pot"
    BRICK = "brick"
    WALL = "wall"
    TOOL = "tool"

class Object(Base):
    __tablename__ = "objects"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    # Store Enum by VALUE (lowercase strings) to match existing DB enum ('objecttype')
    type = Column(SAEnum(ObjectType, values_callable=lambda e: [i.value for i in e], name="objecttype"), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    rotation = Column(Float, default=0.0)
    meta_json = Column(Text)  # JSON string storage for metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    room = relationship("Room", back_populates="objects")
    tools_logs = relationship("ToolsLog", back_populates="target_object")
    
    def get_metadata(self):
        if self.meta_json:
            return json.loads(self.meta_json)
        return {}
    
    def set_metadata(self, data):
        self.meta_json = json.dumps(data)
