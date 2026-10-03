from pydantic import BaseModel


class TechnicianProfileRequest(BaseModel):
    whatsapp_number: str | None = None
    experience_years: int | None = None
    about: str | None = None
    response_time: str | None = None