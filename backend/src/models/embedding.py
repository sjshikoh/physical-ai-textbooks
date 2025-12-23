from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class EmbeddingVectorBase(BaseModel):
    """Base model for embedding vector with common attributes"""
    chapter_id: str = Field(..., min_length=1)
    text_content: str = Field(..., min_length=1)
    vector: List[float] = Field(..., min_length=1)  # Embedding vector as list of floats
    chunk_index: int = Field(..., ge=0)  # Position of this chunk within the chapter


class EmbeddingVectorCreate(EmbeddingVectorBase):
    """Model for creating a new embedding vector"""
    pass


class EmbeddingVectorUpdate(BaseModel):
    """Model for updating an existing embedding vector"""
    text_content: Optional[str] = Field(None, min_length=1)
    vector: Optional[List[float]] = Field(None, min_length=1)
    chunk_index: Optional[int] = Field(None, ge=0)


class EmbeddingVector(EmbeddingVectorBase):
    """Model for a complete embedding vector with database fields"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True