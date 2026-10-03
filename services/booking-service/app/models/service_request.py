from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    Numeric
)
from sqlalchemy.sql import func

from app.database import Base


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

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

    service_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    sub_service_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    technician_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    description = Column(
        String(2000),
        nullable=True
    )

    priority = Column(
        String(30),
        default="Medium",
        nullable=False
    )

    requested_date = Column(
        Date,
        nullable=True
    )

    preferred_time = Column(
        Time,
        nullable=True
    )

    estimated_price = Column(
        Numeric(12, 2),
        nullable=True
    )

    final_price = Column(
        Numeric(12, 2),
        nullable=True
    )

    payment_method = Column(
        String(50),
        nullable=True
    )

    status = Column(
        String(50),
        default="Pending",
        nullable=False,
        index=True
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