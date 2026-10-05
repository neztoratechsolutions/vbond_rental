from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from database import Base


class PropertyAbout(Base):
    __tablename__ = "property_about"

    id = Column(Integer, primary_key=True, index=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        String(2000),
        nullable=True
    )

    preferred_tenant = Column(
        String(100),
        nullable=True
    )

    pets_allowed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    smoking_allowed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    max_occupancy = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )