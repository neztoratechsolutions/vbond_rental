from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.states import router as state_router
from routers.cities import router as city_router
from routers.services import router as service_router
from routers.sub_services import router as sub_service_router
from routers.owner_agreement import router as owner_agreement_router
from routers.property_amenity import router as property_amenity_router
from routers.amenities import router as amenities_router


app = FastAPI(
    title="Rental Platform - Property Service",
    version="1.0.0"
)


app.mount(
    "/uploads",
    StaticFiles(directory="app/uploads"),
    name="uploads"
)


app.include_router(state_router)
app.include_router(city_router)
app.include_router(service_router)
app.include_router(sub_service_router)
app.include_router(owner_agreement_router)
app.include_router(property_amenity_router)
app.include_router(amenities_router)