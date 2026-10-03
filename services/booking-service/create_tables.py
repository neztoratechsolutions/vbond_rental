from app.database import Base, engine

# Import all models so SQLAlchemy registers them
from app.models.booking import Booking
from app.models.booking_history import BookingHistory
from app.models.service_request import ServiceRequest
from app.models.technician_assignment import TechnicianAssignment


print("Creating Booking Service tables...")

Base.metadata.create_all(bind=engine)

print("Booking Service tables created successfully.")