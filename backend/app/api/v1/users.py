"""
User management routes for the Digital Signage API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_admin_user, get_password_hash
from app.models.user import User as UserModel
from app.models.agency import Agency
from app.schemas.user import User, UserCreate, UserUpdate, UserResponse
from app.schemas.agency import AgencyResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all users with pagination"""
    result = await db.execute(
        select(UserModel, Agency.name.label("agency_name"))
        .outerjoin(Agency, UserModel.agency_id == Agency.id)
        .offset(skip)
        .limit(limit)
    )
    users = result.all()

    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            agency_id=user.agency_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            agency_name=agency_name
        )
        for user, agency_name in users
    ]

@router.post("/", response_model=User)
async def create_user(
    user_data: UserCreate,
    current_user: UserModel = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    # Check if user already exists
    result = await db.execute(
        select(UserModel).where(
            (UserModel.username == user_data.username) |
            (UserModel.email == user_data.email)
        )
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role,
        is_active=user_data.is_active,
        agency_id=user_data.agency_id
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific user by ID"""
    result = await db.execute(
        select(UserModel, Agency.name.label("agency_name"))
        .outerjoin(Agency, UserModel.agency_id == Agency.id)
        .where(UserModel.id == user_id)
    )
    user_data = result.first()

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user, agency_name = user_data
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        agency_id=user.agency_id,
        created_at=user.created_at,
        updated_at=user.updated_at,
        agency_name=agency_name
    )

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a user"""
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password" and value:
            setattr(db_user, "hashed_password", get_password_hash(value))
        elif hasattr(db_user, field):
            setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)

    return db_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a user"""
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent deleting yourself
    if db_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    await db.delete(db_user)
    await db.commit()

    return {"message": "User deleted successfully"}
