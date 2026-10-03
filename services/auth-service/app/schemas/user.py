from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    phone: str | None = None