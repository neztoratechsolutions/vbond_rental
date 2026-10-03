from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Numeric
)
from sqlalchemy.sql import func

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # IDs from other services
    property_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    tenant_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    owner_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    booking_date = Column(
        Date,
        nullable=False
    )

    move_in_date = Column(
        Date,
        nullable=True
    )

    rent_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    security_deposit = Column(
        Numeric(12, 2),
        nullable=True
    )

    status = Column(
        String(50),
        default="Pending",
        nullable=False,
        index=True
    )

    remarks = Column(
        String(1000),
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