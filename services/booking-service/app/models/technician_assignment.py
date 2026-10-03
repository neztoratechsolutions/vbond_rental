from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base


class TechnicianAssignment(Base):
    __tablename__ = "technician_assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    service_request_id = Column(
        Integer,
        ForeignKey("service_requests.id"),
        nullable=False,
        index=True
    )

    technician_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    # User ID of admin/owner who assigned technician
    assigned_by = Column(
        Integer,
        nullable=False,
        index=True
    )

    assigned_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    accepted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    remarks = Column(
        String(1000),
        nullable=True
    )