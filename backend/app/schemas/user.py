"""
Pydantic schemas for User model
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    TECHNICIAN = "technician"

class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.TECHNICIAN
    is_active: bool = True
    agency_id: Optional[int] = None

class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    agency_id: Optional[int] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    """Base schema for user in database"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """Schema for user response"""
    pass

class UserResponse(UserInDBBase):
    """Schema for user response (without password)"""
    pass

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for token data"""
    username: Optional[str] = None
