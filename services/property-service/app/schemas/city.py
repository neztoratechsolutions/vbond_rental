from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    state_id: int
    name: str
    is_active: bool = True


class CityUpdate(BaseModel):
    state_id: int | None = None
    name: str | None = None
    is_active: bool | None = None


class CityResponse(BaseModel):
    id: int
    state_id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)