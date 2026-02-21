"""Paper model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Float

from app.core.database import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    doi = Column(String(255), unique=True, index=True)
    pmid = Column(String(50), unique=True, index=True)
    title = Column(Text, nullable=False)
    abstract = Column(Text)
    authors = Column(JSON)
    year = Column(Integer, index=True)
    journal = Column(String(500))
    volume = Column(String(50))
    issue = Column(String(50))
    pages = Column(String(100))
    paper_type = Column(String(50))
    open_access = Column(Boolean, default=False, index=True)
    citation_count = Column(Integer, default=0)
    url = Column(Text)
    sources = Column(JSON)
    embedding = Column(ARRAY(Float))
    summary = Column(Text)
    objectives = Column(Text)
    methodology = Column(Text)
    results = Column(Text)
    limitations = Column(Text)
    practical_implications = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self, include_abstract=True):
        result = {
            "id": self.id, "doi": self.doi, "pmid": self.pmid,
            "title": self.title, "authors": self.authors or [],
            "year": self.year, "journal": self.journal,
            "paper_type": self.paper_type, "open_access": self.open_access,
            "citation_count": self.citation_count, "url": self.url,
            "sources": self.sources or []
        }
        if include_abstract and self.abstract:
            result["abstract"] = self.abstract
        return result