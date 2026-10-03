from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class TenantProfile(Base):
    __tablename__ = "tenant_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True
    )

    whatsapp_number = Column(String(20), nullable=True)

    date_of_birth = Column(Date, nullable=True)

    gender = Column(String(30), nullable=True)

    occupation = Column(String(150), nullable=True)

    address = Column(String(500), nullable=True)

    state_id = Column(Integer, nullable=True)

    city_id = Column(Integer, nullable=True)

    id_type = Column(String(50), nullable=True)

    id_number = Column(String(100), nullable=True)

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