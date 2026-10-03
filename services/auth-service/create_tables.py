from app.database import Base, engine

# Import all models so SQLAlchemy registers them
from app.models.user import User
from app.models.tenant import TenantProfile
# from app.models.tenant_document import TenantDocument
from app.models.technician import TechnicianProfile


print("Creating Auth Service tables...")

Base.metadata.create_all(bind=engine)

print("Auth Service tables created successfully.")