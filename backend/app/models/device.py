"""
Device model for managing Raspberry Pi devices
"""

from sqlalchemy import Column, String, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

class Device(Base):
    """Device model"""

    __tablename__ = "devices"

    name = Column(String(100), nullable=False)
    ip_address = Column(String(45), unique=True, index=True, nullable=False)
    mac_address = Column(String(17), unique=True, index=True, nullable=True)
    agency_id = Column(Integer, nullable=False)  # Foreign key to agencies table
    status = Column(Enum("online", "offline", "maintenance", name="device_statuses"), default="offline")
    last_seen = Column(DateTime(timezone=True), nullable=True)
    version = Column(String(20), default="1.0.0")
    notes = Column(Text, nullable=True)

    # Relationships
    agency = relationship("Agency", back_populates="devices")

    def __repr__(self):
        return f"<Device(id={self.id}, name={self.name}, ip={self.ip_address}, status={self.status})>"
