"""
Pydantic schemas for Schedule model
"""

from typing import Optional, List
from datetime import datetime, time
from pydantic import BaseModel

class ScheduleBase(BaseModel):
    """Base schedule schema"""
    content_id: int
    agency_id: int
    start_time: str  # HH:MM format
    end_time: str    # HH:MM format
    days_of_week: str  # e.g., "1,2,3,4,5" for Mon-Fri
    is_active: bool = True
    priority: int = 1

class ScheduleCreate(ScheduleBase):
    """Schema for creating a schedule"""
    pass

class ScheduleUpdate(BaseModel):
    """Schema for updating a schedule"""
    content_id: Optional[int] = None
    agency_id: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    days_of_week: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None

class ScheduleInDBBase(ScheduleBase):
    """Base schema for schedule in database"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Schedule(ScheduleInDBBase):
    """Schema for schedule response"""
    pass

class ScheduleResponse(ScheduleInDBBase):
    """Schema for schedule response with relationships"""
    content_title: Optional[str] = None
    agency_name: Optional[str] = None

class ScheduleConflict(BaseModel):
    """Schema for schedule conflicts"""
    message: str
    conflicting_schedules: List[int] = []
