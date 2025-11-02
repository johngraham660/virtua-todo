"""
Pydantic models for the TODO application.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re
import html

def sanitize_text(text: str) -> str:
    """Sanitize text input by escaping HTML and removing dangerous characters"""
    if not text:
        return text
    
    # Remove HTML tags and escape HTML entities
    text = html.escape(text.strip())
    
    # Remove any remaining script-like content
    text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
    
    return text

class TaskCreate(BaseModel):
    """Model for creating a new task"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")

    @validator('title')
    def sanitize_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        sanitized = sanitize_text(v)
        if len(sanitized.strip()) == 0:
            raise ValueError('Title cannot be empty after sanitization')
        return sanitized

    @validator('description')
    def sanitize_description(cls, v):
        if v is None:
            return v
        return sanitize_text(v) if v.strip() else None

class TaskUpdate(BaseModel):
    """Model for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")

    @validator('title')
    def sanitize_title(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Title cannot be empty')
        sanitized = sanitize_text(v)
        if len(sanitized.strip()) == 0:
            raise ValueError('Title cannot be empty after sanitization')
        return sanitized

    @validator('description')
    def sanitize_description(cls, v):
        if v is None:
            return v
        return sanitize_text(v) if v.strip() else None

class TaskResponse(BaseModel):
    """Model for task responses"""
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True