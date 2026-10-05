from database import Base, engine

# Import all models so SQLAlchemy registers them
from models.state import State
from models.city import City
from models.property_type import PropertyType
from models.amenity import Amenity
from models.service import Service
from models.sub_service import SubService
from models.property import Property
from models.property_about import PropertyAbout
from models.property_amenity import PropertyAmenity
from models.property_media import PropertyMedia


print("Creating Property Service tables...")

Base.metadata.create_all(bind=engine)

print("Property Service tables created successfully.")