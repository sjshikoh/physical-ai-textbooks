from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class SourceChunk(BaseModel):
    """Model for a source chunk used in RAG responses"""
    chapter_slug: str
    text: str
    similarity_score: float = Field(ge=0.0, le=1.0)


class RAGQueryBase(BaseModel):
    """Base model for RAG query with common attributes"""
    session_id: str = Field(..., min_length=1)
    query_text: str = Field(..., min_length=1, max_length=1000)
    response_text: Optional[str] = Field(None, min_length=1)
    source_chunks: List[SourceChunk] = Field(default_factory=list)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    query_type: str = Field(default="general")  # "general", "text-selection", etc.


class RAGQueryCreate(RAGQueryBase):
    """Model for creating a new RAG query"""
    pass


class RAGQueryUpdate(BaseModel):
    """Model for updating an existing RAG query"""
    response_text: Optional[str] = Field(None, min_length=1)
    source_chunks: Optional[List[SourceChunk]] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class RAGQuery(RAGQueryBase):
    """Model for a complete RAG query with database fields"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True