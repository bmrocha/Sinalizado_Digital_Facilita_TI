"""
Base model for SQLAlchemy models
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

class Base:
    """Base class for all models"""

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Create the base instance
Base = declarative_base(cls=Base)
