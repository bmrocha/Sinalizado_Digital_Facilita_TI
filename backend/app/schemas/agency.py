"""
Pydantic schemas for Agency model
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ScreenOrientation(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

class AgencyBase(BaseModel):
    """Base agency schema"""
    name: str
    code: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo_url: Optional[str] = None
    raspberry_pi_ip: Optional[str] = None
    orientation: ScreenOrientation = ScreenOrientation.HORIZONTAL
    hibernation_enabled: bool = True
    hibernation_start: str = "18:00"
    hibernation_end: str = "08:00"

class AgencyCreate(AgencyBase):
    """Schema for creating an agency"""
    pass

class AgencyUpdate(BaseModel):
    """Schema for updating an agency"""
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo_url: Optional[str] = None
    raspberry_pi_ip: Optional[str] = None
    orientation: Optional[ScreenOrientation] = None
    hibernation_enabled: Optional[bool] = None
    hibernation_start: Optional[str] = None
    hibernation_end: Optional[str] = None

class AgencyInDBBase(AgencyBase):
    """Base schema for agency in database"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Agency(AgencyInDBBase):
    """Schema for agency response"""
    pass

class AgencyResponse(AgencyInDBBase):
    """Schema for agency response with relationships"""
    users_count: Optional[int] = 0
    devices_count: Optional[int] = 0
    contents_count: Optional[int] = 0
