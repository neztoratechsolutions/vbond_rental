from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False, unique=True)

    description = Column(String(500), nullable=True)
    image_url = Column(String(1000), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

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