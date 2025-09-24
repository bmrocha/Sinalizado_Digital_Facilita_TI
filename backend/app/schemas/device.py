"""
Pydantic schemas for Device model
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"

class DeviceBase(BaseModel):
    """Base device schema"""
    name: str
    ip_address: str
    mac_address: Optional[str] = None
    agency_id: int
    status: DeviceStatus = DeviceStatus.OFFLINE
    version: str = "1.0.0"
    notes: Optional[str] = None

class DeviceCreate(DeviceBase):
    """Schema for creating a device"""
    pass

class DeviceUpdate(BaseModel):
    """Schema for updating a device"""
    name: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    agency_id: Optional[int] = None
    status: Optional[DeviceStatus] = None
    version: Optional[str] = None
    notes: Optional[str] = None

class DeviceInDBBase(DeviceBase):
    """Base schema for device in database"""
    id: int
    last_seen: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Device(DeviceInDBBase):
    """Schema for device response"""
    pass

class DeviceResponse(DeviceInDBBase):
    """Schema for device response with relationships"""
    agency_name: Optional[str] = None

class DeviceStatusUpdate(BaseModel):
    """Schema for updating device status"""
    status: DeviceStatus
    last_seen: Optional[datetime] = None
