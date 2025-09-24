"""
Import all schemas for easier access
"""

from app.schemas.user import (
    User, UserCreate, UserUpdate, UserInDBBase, UserResponse,
    UserLogin, Token, TokenData, UserRole
)
from app.schemas.agency import (
    Agency, AgencyCreate, AgencyUpdate, AgencyInDBBase, AgencyResponse,
    ScreenOrientation
)
from app.schemas.content import (
    Content, ContentCreate, ContentUpdate, ContentInDBBase, ContentResponse,
    ContentType
)
from app.schemas.schedule import (
    Schedule, ScheduleCreate, ScheduleUpdate, ScheduleInDBBase, ScheduleResponse,
    ScheduleConflict
)
from app.schemas.device import (
    Device, DeviceCreate, DeviceUpdate, DeviceInDBBase, DeviceResponse,
    DeviceStatusUpdate, DeviceStatus
)

__all__ = [
    # User schemas
    "User", "UserCreate", "UserUpdate", "UserInDBBase", "UserResponse",
    "UserLogin", "Token", "TokenData", "UserRole",
    # Agency schemas
    "Agency", "AgencyCreate", "AgencyUpdate", "AgencyInDBBase", "AgencyResponse",
    "ScreenOrientation",
    # Content schemas
    "Content", "ContentCreate", "ContentUpdate", "ContentInDBBase", "ContentResponse",
    "ContentType",
    # Schedule schemas
    "Schedule", "ScheduleCreate", "ScheduleUpdate", "ScheduleInDBBase", "ScheduleResponse",
    "ScheduleConflict",
    # Device schemas
    "Device", "DeviceCreate", "DeviceUpdate", "DeviceInDBBase", "DeviceResponse",
    "DeviceStatusUpdate", "DeviceStatus"
]
