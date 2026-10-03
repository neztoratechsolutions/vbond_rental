from pydantic import BaseModel
from datetime import date


class TenantProfileRequest(BaseModel):
    whatsapp_number: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    occupation: str | None = None
    address: str | None = None
    state_id: int | None = None
    city_id: int | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    id_type: str | None = None
    id_number: str | None = None