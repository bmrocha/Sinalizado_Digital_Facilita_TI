"""
Main API router that includes all v1 API routes
"""

from fastapi import APIRouter
from app.api.v1 import auth, users, agencies, contents, schedules, devices

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(agencies.router, prefix="/agencies", tags=["agencies"])
api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
