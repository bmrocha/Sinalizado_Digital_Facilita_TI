"""
Content model for managing digital signage content
"""

from sqlalchemy import Column, String, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

class Content(Base):
    """Content model"""

    __tablename__ = "contents"

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(Enum("link", "image", "video", name="content_types"), nullable=False)
    url = Column(String(500), nullable=True)  # For links and media files
    file_path = Column(String(255), nullable=True)  # Local file path for uploaded content
    duration = Column(Integer, default=30)  # Duration in seconds (for videos and images)
    is_active = Column(Boolean, default=True)
    agency_id = Column(Integer, nullable=False)  # Foreign key to agencies table

    # Relationships
    agency = relationship("Agency", back_populates="contents")
    schedules = relationship("Schedule", back_populates="content")

    def __repr__(self):
        return f"<Content(id={self.id}, title={self.title}, type={self.content_type})>"
