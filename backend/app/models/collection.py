"""Collection model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    saved_papers = relationship("SavedPaper", back_populates="collection", cascade="all, delete-orphan")
    user = relationship("User")

    def to_dict(self):
        return {
            "id": self.id, "user_id": self.user_id, "name": self.name,
            "description": self.description, "paper_count": len(self.saved_papers) if self.saved_papers else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }