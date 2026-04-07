from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)

    project_name = Column(String, nullable=False)
    branch = Column(String, default="main")
    commit_hash = Column(String, nullable=False)
    pipeline_name = Column(String)

    status = Column(String, default="pending")  # pending, success, failed
    classification = Column(String)  # "Dependency Conflict"
    confidence = Column(Float)
    error_type = Column(String)  # "Permission", "Timeout" etc.

    log_fragment = Column(Text)  # raw log
    ai_reason = Column(Text)
    ai_steps = Column(JSON)  # string list

    analysis_time_sec = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    notes = relationship("AnalysisNote", back_populates="analysis", cascade="all, delete-orphan")


class AnalysisNote(Base):
    __tablename__ = "analysis_notes"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analysis = relationship("Analysis", back_populates="notes")