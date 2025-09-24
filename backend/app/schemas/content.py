"""
Pydantic schemas for Content model
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ContentType(str, Enum):
    LINK = "link"
    IMAGE = "image"
    VIDEO = "video"

class ContentBase(BaseModel):
    """Base content schema"""
    title: str
    description: Optional[str] = None
    content_type: ContentType
    url: Optional[str] = None
    file_path: Optional[str] = None
    duration: int = 30
    is_active: bool = True
    agency_id: int

class ContentCreate(ContentBase):
    """Schema for creating content"""
    pass

class ContentUpdate(BaseModel):
    """Schema for updating content"""
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[ContentType] = None
    url: Optional[str] = None
    file_path: Optional[str] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None
    agency_id: Optional[int] = None

class ContentInDBBase(ContentBase):
    """Base schema for content in database"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Content(ContentInDBBase):
    """Schema for content response"""
    pass

class ContentResponse(ContentInDBBase):
    """Schema for content response with relationships"""
    agency_name: Optional[str] = None
    schedules_count: Optional[int] = 0
