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


class PropertyMedia(Base):
    __tablename__ = "property_media"

    id = Column(Integer, primary_key=True, index=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        nullable=False,
        index=True
    )

    media_type = Column(
        String(50),
        nullable=False
    )

    file_url = Column(
        String(1000),
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=True
    )

    is_primary = Column(
        Boolean,
        default=False,
        nullable=False
    )

    display_order = Column(
        Integer,
        default=0,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )