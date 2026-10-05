from pydantic import BaseModel, ConfigDict


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str | None
    image_url: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)



#------------------Sub Services----------------#



class SubServiceCreate(BaseModel):
    service_id: int
    name: str
    description: str | None = None
    is_active: bool = True


class SubServiceUpdate(BaseModel):
    service_id: int | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class SubServiceResponse(BaseModel):
    id: int
    service_id: int
    name: str
    description: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)