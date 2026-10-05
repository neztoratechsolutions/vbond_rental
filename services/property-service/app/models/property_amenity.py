from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class PropertyAmenity(Base):
    __tablename__ = "property_amenities"

    id = Column(Integer, primary_key=True, index=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        nullable=False,
        index=True
    )

    amenity_id = Column(
        Integer,
        ForeignKey("amenities.id"),
        nullable=False,
        index=True
    )