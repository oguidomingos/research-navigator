"""User model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class PlanType(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    plan = Column(Enum(PlanType), default=PlanType.FREE, nullable=False)
    daily_search_limit = Column(Integer, default=10)
    daily_summary_limit = Column(Integer, default=5)
    max_collections = Column(Integer, default=5)
    max_saved_articles = Column(Integer, default=50)
    can_upload_pdf = Column(Boolean, default=False)
    preferred_language = Column(String(10), default="pt")
    citation_style = Column(String(10), default="ABNT")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))

    def to_dict(self):
        return {
            "id": self.id, "email": self.email, "name": self.name,
            "plan": self.plan.value, "preferred_language": self.preferred_language
        }