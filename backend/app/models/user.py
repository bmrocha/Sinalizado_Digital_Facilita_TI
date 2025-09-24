"""
User model for authentication and authorization
"""

from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    """User model"""

    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "manager", "technician", name="user_roles"), nullable=False, default="technician")
    is_active = Column(Boolean, default=True)
    agency_id = Column(Integer, nullable=True)  # Foreign key to agencies table

    # Relationships
    agency = relationship("Agency", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
