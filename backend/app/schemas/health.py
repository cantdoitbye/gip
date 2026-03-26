from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str


class ServicesHealth(BaseModel):
    database: str
    redis: str


class DetailedHealthResponse(BaseModel):
    status: str
    version: str
    services: ServicesHealth
