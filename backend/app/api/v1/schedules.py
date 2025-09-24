"""
Schedule management routes for the Digital Signage API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import datetime, time
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.schedule import Schedule
from app.models.content import Content
from app.models.agency import Agency
from app.schemas.schedule import Schedule, ScheduleCreate, ScheduleUpdate, ScheduleResponse, ScheduleConflict

router = APIRouter()

def check_schedule_conflict(
    start_time: time,
    end_time: time,
    days_of_week: str,
    agency_id: int,
    exclude_schedule_id: int = None
) -> str:
    """Check for schedule conflicts"""
    # This would be implemented with database queries to check for overlapping schedules
    # For now, return empty string if no conflict
    return ""

@router.get("/", response_model=List[ScheduleResponse])
async def get_schedules(
    skip: int = 0,
    limit: int = 100,
    agency_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all schedules with optional agency filter"""
    query = select(Schedule, Content.title.label("content_title"), Agency.name.label("agency_name")) \
        .join(Content, Schedule.content_id == Content.id) \
        .join(Agency, Schedule.agency_id == Agency.id)

    if agency_id:
        query = query.where(Schedule.agency_id == agency_id)

    result = await db.execute(query.offset(skip).limit(limit))
    schedules = result.all()

    return [
        ScheduleResponse(
            id=schedule.id,
            content_id=schedule.content_id,
            agency_id=schedule.agency_id,
            start_time=str(schedule.start_time),
            end_time=str(schedule.end_time),
            days_of_week=schedule.days_of_week,
            is_active=schedule.is_active,
            priority=schedule.priority,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
            content_title=content_title,
            agency_name=agency_name
        )
        for schedule, content_title, agency_name in schedules
    ]

@router.post("/", response_model=Schedule)
async def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new schedule"""
    # Verify content and agency exist
    result = await db.execute(
        select(Content).where(Content.id == schedule_data.content_id)
    )
    content = result.scalar_one_or_none()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    result = await db.execute(
        select(Agency).where(Agency.id == schedule_data.agency_id)
    )
    agency = result.scalar_one_or_none()

    if not agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

    # Check for conflicts
    conflict_message = check_schedule_conflict(
        schedule_data.start_time,
        schedule_data.end_time,
        schedule_data.days_of_week,
        schedule_data.agency_id
    )

    if conflict_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=conflict_message
        )

    # Create schedule
    db_schedule = Schedule(**schedule_data.dict())
    db.add(db_schedule)
    await db.commit()
    await db.refresh(db_schedule)

    return db_schedule

@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific schedule by ID"""
    result = await db.execute(
        select(Schedule, Content.title.label("content_title"), Agency.name.label("agency_name"))
        .join(Content, Schedule.content_id == Content.id)
        .join(Agency, Schedule.agency_id == Agency.id)
        .where(Schedule.id == schedule_id)
    )
    schedule_data = result.first()

    if not schedule_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    schedule, content_title, agency_name = schedule_data
    return ScheduleResponse(
        id=schedule.id,
        content_id=schedule.content_id,
        agency_id=schedule.agency_id,
        start_time=str(schedule.start_time),
        end_time=str(schedule.end_time),
        days_of_week=schedule.days_of_week,
        is_active=schedule.is_active,
        priority=schedule.priority,
        created_at=schedule.created_at,
        updated_at=schedule.updated_at,
        content_title=content_title,
        agency_name=agency_name
    )

@router.put("/{schedule_id}", response_model=Schedule)
async def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a schedule"""
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    db_schedule = result.scalar_one_or_none()

    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    # Update schedule fields
    for field, value in schedule_update.dict(exclude_unset=True).items():
        if hasattr(db_schedule, field):
            setattr(db_schedule, field, value)

    await db.commit()
    await db.refresh(db_schedule)

    return db_schedule

@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a schedule"""
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    db_schedule = result.scalar_one_or_none()

    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    await db.delete(db_schedule)
    await db.commit()

    return {"message": "Schedule deleted successfully"}

@router.get("/agency/{agency_id}/current")
async def get_current_schedule(
    agency_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current schedule for an agency based on current time and day"""
    now = datetime.now()
    current_time = now.time()
    current_weekday = now.weekday() + 1  # Monday = 1, Sunday = 7

    # Get active schedules for this agency and day
    result = await db.execute(
        select(Schedule, Content.title.label("content_title"), Content.content_type, Content.url, Content.file_path)
        .join(Content, Schedule.content_id == Content.id)
        .where(
            and_(
                Schedule.agency_id == agency_id,
                Schedule.is_active == True,
                Schedule.start_time <= current_time,
                Schedule.end_time >= current_time,
                Schedule.days_of_week.contains(str(current_weekday))
            )
        )
        .order_by(Schedule.priority.desc())
    )

    schedules = result.all()

    if not schedules:
        return {"message": "No active schedule found for current time"}

    # Return the highest priority schedule
    schedule, content_title, content_type, url, file_path = schedules[0]
    return {
        "schedule_id": schedule.id,
        "content_id": schedule.content_id,
        "content_title": content_title,
        "content_type": content_type,
        "url": url,
        "file_path": file_path,
        "duration": 30,  # Default duration, should come from content
        "start_time": str(schedule.start_time),
        "end_time": str(schedule.end_time)
    }
