"""
Authentication routes for the Digital Signage API
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, settings
)
from app.schemas.user import User, UserCreate, UserUpdate, Token, UserLogin
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return JWT token"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    result = await db.execute(
        UserModel.__table__.select().where(
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

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_active_user)
):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user information"""
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password" and value:
            setattr(current_user, "hashed_password", get_password_hash(value))
        elif hasattr(current_user, field):
            setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user
