from pydantic import BaseModel, ConfigDict


class StateCreate(BaseModel):
    name: str
    code: str | None = None
    is_active: bool = True


class StateUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    is_active: bool | None = None


class StateResponse(BaseModel):
    id: int
    name: str
    code: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)