"""
Schedule model for managing content display schedules
"""

from sqlalchemy import Column, String, Boolean, DateTime, Time
from sqlalchemy.orm import relationship
from app.models.base import Base

class Schedule(Base):
    """Schedule model"""

    __tablename__ = "schedules"

    content_id = Column(Integer, nullable=False)  # Foreign key to contents table
    agency_id = Column(Integer, nullable=False)   # Foreign key to agencies table
    start_time = Column(Time, nullable=False)     # HH:MM format
    end_time = Column(Time, nullable=False)       # HH:MM format
    days_of_week = Column(String(20), nullable=False)  # e.g., "1,2,3,4,5" for Mon-Fri
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=1)         # Higher number = higher priority

    # Relationships
    agency = relationship("Agency", back_populates="schedules")
    content = relationship("Content", back_populates="schedules")

    def __repr__(self):
        return f"<Schedule(id={self.id}, content_id={self.content_id}, days={self.days_of_week})>"
