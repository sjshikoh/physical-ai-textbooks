from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class ChapterBase(BaseModel):
    """Base model for textbook chapter with common attributes"""
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    order: int = Field(..., ge=1, le=6)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ChapterCreate(ChapterBase):
    """Model for creating a new textbook chapter"""
    pass


class ChapterUpdate(BaseModel):
    """Model for updating an existing textbook chapter"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    order: Optional[int] = Field(None, ge=1, le=6)
    metadata: Optional[Dict[str, Any]] = None


class Chapter(ChapterBase):
    """Model for a complete textbook chapter with database fields"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True