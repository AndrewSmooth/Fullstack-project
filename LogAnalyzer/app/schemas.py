from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List


class AnalysisCreate(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=100)
    branch: str = Field(default="main", max_length=50)
    commit_hash: str = Field(..., min_length=7, max_length=40)
    pipeline_name: Optional[str] = Field(default=None, max_length=100)
    log_fragment: Optional[str] = Field(default=None, max_length=10000)

    @field_validator('commit_hash')
    @classmethod
    def validate_commit_hash(cls, v):
        if not v.isalnum():
            raise ValueError('commit_hash должен содержать только буквы и цифры')
        return v


class AnalysisUpdate(BaseModel):
    project_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    branch: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, pattern="^(pending|success|failed|error)$")
    classification: Optional[str] = Field(default=None, max_length=100)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    error_type: Optional[str] = Field(default=None, max_length=50)
    ai_reason: Optional[str] = Field(default=None)
    ai_steps: Optional[List[str]] = None
    analysis_time_sec: Optional[float] = Field(default=None, ge=0)


class AnalysisResponse(BaseModel):
    id: int
    project_name: str
    branch: str
    commit_hash: str
    pipeline_name: Optional[str]
    status: str
    classification: Optional[str]
    confidence: Optional[float]
    error_type: Optional[str]
    log_fragment: Optional[str]
    ai_reason: Optional[str]
    ai_steps: Optional[List[str]]
    analysis_time_sec: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

# pagination
class AnalysisListResponse(BaseModel):
    items: List[AnalysisResponse]
    total: int
    page: int
    limit: int


class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class NoteResponse(BaseModel):
    id: int
    analysis_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True