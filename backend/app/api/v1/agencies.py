"""
Agency management routes for the Digital Signage API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import os
import uuid
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.agency import Agency
from app.models.user import User
from app.models.device import Device
from app.models.content import Content
from app.schemas.agency import Agency, AgencyCreate, AgencyUpdate, AgencyResponse
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[AgencyResponse])
async def get_agencies(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all agencies with counts"""
    result = await db.execute(
        select(
            Agency,
            func.count(User.id).label("users_count"),
            func.count(Device.id).label("devices_count"),
            func.count(Content.id).label("contents_count")
        )
        .outerjoin(User, Agency.id == User.agency_id)
        .outerjoin(Device, Agency.id == Device.agency_id)
        .outerjoin(Content, Agency.id == Content.agency_id)
        .group_by(Agency.id)
        .offset(skip)
        .limit(limit)
    )
    agencies = result.all()

    return [
        AgencyResponse(
            id=agency.id,
            name=agency.name,
            code=agency.code,
            address=agency.address,
            city=agency.city,
            state=agency.state,
            phone=agency.phone,
            email=agency.email,
            logo_url=agency.logo_url,
            raspberry_pi_ip=agency.raspberry_pi_ip,
            orientation=agency.orientation,
            hibernation_enabled=agency.hibernation_enabled,
            hibernation_start=agency.hibernation_start,
            hibernation_end=agency.hibernation_end,
            created_at=agency.created_at,
            updated_at=agency.updated_at,
            users_count=users_count,
            devices_count=devices_count,
            contents_count=contents_count
        )
        for agency, users_count, devices_count, contents_count in agencies
    ]

@router.post("/", response_model=Agency)
async def create_agency(
    agency_data: AgencyCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new agency"""
    # Check if agency code already exists
    result = await db.execute(
        select(Agency).where(Agency.code == agency_data.code)
    )
    existing_agency = result.scalar_one_or_none()

    if existing_agency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agency code already exists"
        )

    # Create new agency
    db_agency = Agency(**agency_data.dict())
    db.add(db_agency)
    await db.commit()
    await db.refresh(db_agency)

    return db_agency

@router.get("/{agency_id}", response_model=AgencyResponse)
async def get_agency(
    agency_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific agency by ID"""
    result = await db.execute(
        select(
            Agency,
            func.count(User.id).label("users_count"),
            func.count(Device.id).label("devices_count"),
            func.count(Content.id).label("contents_count")
        )
        .outerjoin(User, Agency.id == User.agency_id)
        .outerjoin(Device, Agency.id == Device.agency_id)
        .outerjoin(Content, Agency.id == Content.agency_id)
        .where(Agency.id == agency_id)
        .group_by(Agency.id)
    )
    agency_data = result.first()

    if not agency_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

    agency, users_count, devices_count, contents_count = agency_data
    return AgencyResponse(
        id=agency.id,
        name=agency.name,
        code=agency.code,
        address=agency.address,
        city=agency.city,
        state=agency.state,
        phone=agency.phone,
        email=agency.email,
        logo_url=agency.logo_url,
        raspberry_pi_ip=agency.raspberry_pi_ip,
        orientation=agency.orientation,
        hibernation_enabled=agency.hibernation_enabled,
        hibernation_start=agency.hibernation_start,
        hibernation_end=agency.hibernation_end,
        created_at=agency.created_at,
        updated_at=agency.updated_at,
        users_count=users_count,
        devices_count=devices_count,
        contents_count=contents_count
    )

@router.put("/{agency_id}", response_model=Agency)
async def update_agency(
    agency_id: int,
    agency_update: AgencyUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update an agency"""
    result = await db.execute(select(Agency).where(Agency.id == agency_id))
    db_agency = result.scalar_one_or_none()

    if not db_agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

    # Update agency fields
    for field, value in agency_update.dict(exclude_unset=True).items():
        if hasattr(db_agency, field):
            setattr(db_agency, field, value)

    await db.commit()
    await db.refresh(db_agency)

    return db_agency

@router.delete("/{agency_id}")
async def delete_agency(
    agency_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete an agency"""
    result = await db.execute(select(Agency).where(Agency.id == agency_id))
    db_agency = result.scalar_one_or_none()

    if not db_agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

    # Check if agency has users, devices, or content
    result = await db.execute(
        select(func.count()).select_from(
            select(User.id).where(User.agency_id == agency_id).union_all(
                select(Device.id).where(Device.agency_id == agency_id).union_all(
                    select(Content.id).where(Content.agency_id == agency_id)
                )
            )
        )
    )
    total_count = result.scalar()

    if total_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete agency with associated users, devices, or content"
        )

    await db.delete(db_agency)
    await db.commit()

    return {"message": "Agency deleted successfully"}

@router.post("/{agency_id}/upload-logo")
async def upload_logo(
    agency_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload logo for an agency"""
    # Check if agency exists
    result = await db.execute(select(Agency).where(Agency.id == agency_id))
    db_agency = result.scalar_one_or_none()

    if not db_agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, "logos", unique_filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Update agency logo URL
    db_agency.logo_url = f"/uploads/logos/{unique_filename}"
    await db.commit()
    await db.refresh(db_agency)

    return {"message": "Logo uploaded successfully", "logo_url": db_agency.logo_url}

@router.get("/{agency_id}/logo")
async def get_logo(
    agency_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agency logo"""
    result = await db.execute(select(Agency).where(Agency.id == agency_id))
    db_agency = result.scalar_one_or_none()

    if not db_agency or not db_agency.logo_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logo not found"
        )

    logo_path = os.path.join(settings.UPLOAD_DIR, db_agency.logo_url.replace("/uploads/", ""))
    if not os.path.exists(logo_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logo file not found"
        )

    return FileResponse(logo_path)
