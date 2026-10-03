from app.database import Base, engine

# Import all models so SQLAlchemy registers them
from app.models.state import State
from app.models.city import City
from app.models.property_type import PropertyType
from app.models.amenity import Amenity
from app.models.service import Service
from app.models.sub_service import SubService
from app.models.property import Property
from app.models.property_about import PropertyAbout
from app.models.property_amenity import PropertyAmenity
from app.models.property_media import PropertyMedia


print("Creating Property Service tables...")

Base.metadata.create_all(bind=engine)

print("Property Service tables created successfully.")