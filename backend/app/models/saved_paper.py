"""SavedPaper model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SavedPaper(Base):
    __tablename__ = "saved_papers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="CASCADE"), nullable=False, index=True)
    notes = Column(Text)
    tags = Column(JSON)
    save_reason = Column(String(255))
    rating = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    paper = relationship("Paper")
    collection = relationship("Collection", back_populates="saved_papers")
    user = relationship("User")

    def to_dict(self):
        return {
            "id": self.id, "user_id": self.user_id, "paper_id": self.paper_id,
            "collection_id": self.collection_id, "notes": self.notes,
            "tags": self.tags or [], "save_reason": self.save_reason,
            "rating": self.rating, "created_at": self.created_at.isoformat() if self.created_at else None,
            "paper": self.paper.to_dict() if self.paper else None
        }