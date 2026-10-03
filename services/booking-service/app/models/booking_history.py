from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base


class BookingHistory(Base):
    __tablename__ = "booking_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
        index=True
    )

    status = Column(
        String(50),
        nullable=False
    )

    # User ID from Auth Service
    changed_by = Column(
        Integer,
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