from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class UserSessionBase(BaseModel):
    """Base model for user session with common attributes"""
    user_id: Optional[str] = Field(None, min_length=1)  # For authenticated users
    session_token: str = Field(default_factory=lambda: str(uuid.uuid4()))  # For anonymous users
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UserSessionCreate(UserSessionBase):
    """Model for creating a new user session"""
    pass


class UserSessionUpdate(BaseModel):
    """Model for updating an existing user session"""
    preferences: Optional[Dict[str, Any]] = None


class UserSession(UserSessionBase):
    """Model for a complete user session with database fields"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True