from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func

from database import Base


class OwnerAgreement(Base):
    __tablename__ = "owner_agreements"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    # Full agreement content
    agreement_content = Column(
        Text,
        nullable=True
    )

    # Uploaded PDF file path
    agreement_pdf = Column(
        String(500),
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