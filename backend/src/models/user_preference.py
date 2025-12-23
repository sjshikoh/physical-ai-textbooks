from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class UserPreferenceBase(BaseModel):
    """Base model for user preference with common attributes"""
    session_id: str = Field(..., min_length=1)
    preference_key: str = Field(..., min_length=1, max_length=100)
    preference_value: str = Field(..., min_length=1, max_length=500)


class UserPreferenceCreate(UserPreferenceBase):
    """Model for creating a new user preference"""
    pass


class UserPreferenceUpdate(BaseModel):
    """Model for updating an existing user preference"""
    preference_value: Optional[str] = Field(None, min_length=1, max_length=500)


class UserPreference(UserPreferenceBase):
    """Model for a complete user preference with database fields"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True