"""
Agency model for managing different Sicoob branches
"""

from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base

class Agency(Base):
    """Agency model"""

    __tablename__ = "agencies"

    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, index=True, nullable=False)  # Agency code (e.g., "001", "002")
    address = Column(Text, nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(2), nullable=True)  # State abbreviation (e.g., "SP", "RJ")
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    logo_url = Column(String(255), nullable=True)  # Path to agency logo
    raspberry_pi_ip = Column(String(45), nullable=True)  # IP address of Raspberry Pi
    orientation = Column(Enum("horizontal", "vertical", name="screen_orientations"), default="horizontal")
    hibernation_enabled = Column(Boolean, default=True)
    hibernation_start = Column(String(5), default="18:00")  # HH:MM format
    hibernation_end = Column(String(5), default="08:00")    # HH:MM format

    # Relationships
    users = relationship("User", back_populates="agency")
    devices = relationship("Device", back_populates="agency")
    contents = relationship("Content", back_populates="agency")
    schedules = relationship("Schedule", back_populates="agency")

    def __repr__(self):
        return f"<Agency(id={self.id}, name={self.name}, code={self.code})>"
