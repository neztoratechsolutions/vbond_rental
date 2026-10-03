from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Numeric,
    ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)

    # User ID from Auth Service
    owner_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    property_type_id = Column(
        Integer,
        ForeignKey("property_types.id"),
        nullable=False,
        index=True
    )

    state_id = Column(
        Integer,
        ForeignKey("states.id"),
        nullable=False,
        index=True
    )

    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=False,
        index=True
    )

    property_name = Column(
        String(200),
        nullable=False
    )

    full_address = Column(
        String(1000),
        nullable=False
    )

    floor = Column(
        String(50),
        nullable=True
    )

    facing = Column(
        String(50),
        nullable=True
    )

    property_age = Column(
        Integer,
        nullable=True
    )

    built_up_area = Column(
        Numeric(10, 2),
        nullable=True
    )

    carpet_area = Column(
        Numeric(10, 2),
        nullable=True
    )

    bedrooms = Column(
        Integer,
        nullable=True
    )

    bathrooms = Column(
        Integer,
        nullable=True
    )

    balcony = Column(
        Integer,
        nullable=True
    )

    furnishing_status = Column(
        String(50),
        nullable=True
    )

    property_status = Column(
        String(50),
        default="Available",
        nullable=False,
        index=True
    )

    monthly_rent = Column(
        Numeric(12, 2),
        nullable=False
    )

    security_deposit = Column(
        Numeric(12, 2),
        nullable=True
    )

    maintenance_charges = Column(
        Numeric(12, 2),
        nullable=True
    )

    available_from = Column(
        Date,
        nullable=True
    )

    agreement_type = Column(
        String(100),
        nullable=True
    )

    negotiable = Column(
        Boolean,
        default=False,
        nullable=False
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