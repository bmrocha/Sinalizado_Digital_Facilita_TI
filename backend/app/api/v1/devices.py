"""
Device management routes for the Digital Signage API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.device import Device
from app.models.agency import Agency
from app.schemas.device import Device, DeviceCreate, DeviceUpdate, DeviceResponse, DeviceStatusUpdate

router = APIRouter()

@router.get("/", response_model=List[DeviceResponse])
async def get_devices(
    skip: int = 0,
    limit: int = 100,
    agency_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all devices with optional agency filter"""
    query = select(Device, Agency.name.label("agency_name")).join(Agency, Device.agency_id == Agency.id)

    if agency_id:
        query = query.where(Device.agency_id == agency_id)

    result = await db.execute(query.offset(skip).limit(limit))
    devices = result.all()

    return [
        DeviceResponse(
            id=device.id,
            name=device.name,
            ip_address=device.ip_address,
            mac_address=device.mac_address,
            agency_id=device.agency_id,
            status=device.status,
            last_seen=device.last_seen,
            version=device.version,
            notes=device.notes,
            created_at=device.created_at,
            updated_at=device.updated_at,
            agency_name=agency_name
        )
        for device, agency_name in devices
    ]

@router.post("/", response_model=Device)
async def create_device(
    device_data: DeviceCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new device"""
    # Verify agency exists
    result = await db.execute(select(Agency).where(Agency.id == device_data.agency_id))
    agency = result.scalar_one_or_none()

    if not agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found"
        )

    # Check if IP address already exists
    result = await db.execute(
        select(Device).where(Device.ip_address == device_data.ip_address)
    )
    existing_device = result.scalar_one_or_none()

    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device with this IP address already exists"
        )

    # Create device
    db_device = Device(**device_data.dict())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)

    return db_device

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific device by ID"""
    result = await db.execute(
        select(Device, Agency.name.label("agency_name"))
        .join(Agency, Device.agency_id == Agency.id)
        .where(Device.id == device_id)
    )
    device_data = result.first()

    if not device_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    device, agency_name = device_data
    return DeviceResponse(
        id=device.id,
        name=device.name,
        ip_address=device.ip_address,
        mac_address=device.mac_address,
        agency_id=device.agency_id,
        status=device.status,
        last_seen=device.last_seen,
        version=device.version,
        notes=device.notes,
        created_at=device.created_at,
        updated_at=device.updated_at,
        agency_name=agency_name
    )

@router.put("/{device_id}", response_model=Device)
async def update_device(
    device_id: int,
    device_update: DeviceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a device"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    db_device = result.scalar_one_or_none()

    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    # Update device fields
    for field, value in device_update.dict(exclude_unset=True).items():
        if hasattr(db_device, field):
            setattr(db_device, field, value)

    await db.commit()
    await db.refresh(db_device)

    return db_device

@router.delete("/{device_id}")
async def delete_device(
    device_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a device"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    db_device = result.scalar_one_or_none()

    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    await db.delete(db_device)
    await db.commit()

    return {"message": "Device deleted successfully"}

@router.post("/{device_id}/status", response_model=Device)
async def update_device_status(
    device_id: int,
    status_update: DeviceStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update device status (used by Raspberry Pi devices)"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    db_device = result.scalar_one_or_none()

    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    # Update status and last seen
    db_device.status = status_update.status
    db_device.last_seen = status_update.last_seen or datetime.utcnow()

    await db.commit()
    await db.refresh(db_device)

    return db_device

@router.get("/agency/{agency_id}/status")
async def get_agency_devices_status(
    agency_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get status of all devices for an agency"""
    result = await db.execute(
        select(Device)
        .where(Device.agency_id == agency_id)
        .order_by(Device.last_seen.desc())
    )
    devices = result.scalars().all()

    return {
        "agency_id": agency_id,
        "total_devices": len(devices),
        "online_devices": len([d for d in devices if d.status == "online"]),
        "offline_devices": len([d for d in devices if d.status == "offline"]),
        "maintenance_devices": len([d for d in devices if d.status == "maintenance"]),
        "devices": [
            {
                "id": device.id,
                "name": device.name,
                "ip_address": device.ip_address,
                "status": device.status,
                "last_seen": device.last_seen,
                "version": device.version
            }
            for device in devices
        ]
    }
