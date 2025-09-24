"""
Content management routes for the Digital Signage API
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
from app.models.content import Content
from app.models.agency import Agency
from app.models.schedule import Schedule
from app.schemas.content import Content, ContentCreate, ContentUpdate, ContentResponse
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[ContentResponse])
async def get_contents(
    skip: int = 0,
    limit: int = 100,
    agency_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all contents with optional agency filter"""
    query = select(Content, Agency.name.label("agency_name")).join(Agency, Content.agency_id == Agency.id)

    if agency_id:
        query = query.where(Content.agency_id == agency_id)

    result = await db.execute(
        query
        .add_columns(func.count(Schedule.id).label("schedules_count"))
        .outerjoin(Schedule, Content.id == Schedule.content_id)
        .group_by(Content.id, Agency.name)
        .offset(skip)
        .limit(limit)
    )
    contents = result.all()

    return [
        ContentResponse(
            id=content.id,
            title=content.title,
            description=content.description,
            content_type=content.content_type,
            url=content.url,
            file_path=content.file_path,
            duration=content.duration,
            is_active=content.is_active,
            agency_id=content.agency_id,
            created_at=content.created_at,
            updated_at=content.updated_at,
            agency_name=agency_name,
            schedules_count=schedules_count
        )
        for content, agency_name, schedules_count in contents
    ]

@router.post("/", response_model=Content)
async def create_content(
    content_data: ContentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new content"""
    # Verify agency exists
    result = await db.execute(select(Agency).where(Agency.id == content_data.agency_id))
    agency = result.scalar_one_or_none()

    if not agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

    # Create content
    db_content = Content(**content_data.dict())
    db.add(db_content)
    await db.commit()
    await db.refresh(db_content)

    return db_content

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific content by ID"""
    result = await db.execute(
        select(Content, Agency.name.label("agency_name"))
        .join(Agency, Content.agency_id == Agency.id)
        .where(Content.id == content_id)
        .add_columns(func.count(Schedule.id).label("schedules_count"))
        .outerjoin(Schedule, Content.id == Schedule.content_id)
        .group_by(Content.id, Agency.name)
    )
    content_data = result.first()

    if not content_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    content, agency_name, schedules_count = content_data
    return ContentResponse(
        id=content.id,
        title=content.title,
        description=content.description,
        content_type=content.content_type,
        url=content.url,
        file_path=content.file_path,
        duration=content.duration,
        is_active=content.is_active,
        agency_id=content.agency_id,
        created_at=content.created_at,
        updated_at=content.updated_at,
        agency_name=agency_name,
        schedules_count=schedules_count
    )

@router.put("/{content_id}", response_model=Content)
async def update_content(
    content_id: int,
    content_update: ContentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update content"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    db_content = result.scalar_one_or_none()

    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Update content fields
    for field, value in content_update.dict(exclude_unset=True).items():
        if hasattr(db_content, field):
            setattr(db_content, field, value)

    await db.commit()
    await db.refresh(db_content)

    return db_content

@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete content"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    db_content = result.scalar_one_or_none()

    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Check if content has schedules
    result = await db.execute(
        select(func.count()).select_from(
            select(Schedule.id).where(Schedule.content_id == content_id)
        )
    )
    schedules_count = result.scalar()

    if schedules_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete content with associated schedules"
        )

    # Delete file if exists
    if db_content.file_path:
        file_path = os.path.join(settings.UPLOAD_DIR, db_content.file_path.replace("/uploads/", ""))
        if os.path.exists(file_path):
            os.remove(file_path)

    await db.delete(db_content)
    await db.commit()

    return {"message": "Content deleted successfully"}

@router.post("/{content_id}/upload")
async def upload_content_file(
    content_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload file for content"""
    # Check if content exists
    result = await db.execute(select(Content).where(Content.id == content_id))
    db_content = result.scalar_one_or_none()

    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Validate file type based on content type
    if db_content.content_type == "image" and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image for image content"
        )
    elif db_content.content_type == "video" and not file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a video for video content"
        )

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, "contents", unique_filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Update content
    db_content.file_path = f"/uploads/contents/{unique_filename}"
    await db.commit()
    await db.refresh(db_content)

    return {"message": "File uploaded successfully", "file_path": db_content.file_path}

@router.get("/{content_id}/file")
async def get_content_file(
    content_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get content file"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    db_content = result.scalar_one_or_none()

    if not db_content or not db_content.file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content file not found"
        )

    file_path = os.path.join(settings.UPLOAD_DIR, db_content.file_path.replace("/uploads/", ""))
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content file not found on disk"
        )

    return FileResponse(file_path)
