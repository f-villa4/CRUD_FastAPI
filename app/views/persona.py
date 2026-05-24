from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class PersonaBase(BaseModel):
    """Shared attributes for Persona inputs."""
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    birth_date: date | None = None
    is_active: bool = True
    notes: str | None = None


class PersonaCreate(PersonaBase):
    """Schema used for creating a new Persona."""
    pass


class PersonaUpdate(BaseModel):
    """Schema used for partial update of Persona."""
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    birth_date: date | None = None
    is_active: bool | None = None
    notes: str | None = None


class PersonaRead(BaseModel):
    """Schema used to return Persona data to clients."""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    birth_date: date | None
    is_active: bool
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PersonaLabRead(BaseModel):
    """Persona payload for lab endpoints (no created_at)."""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    birth_date: date | None
    is_active: bool
    notes: str | None

    model_config = {"from_attributes": True}

    
class PersonaActivaReport(BaseModel):
    """Projection for active users report."""

    id: int
    email: EmailStr
    phone: str | None
    is_active: bool

    model_config = {"from_attributes": True}

class BulkDesactivarRequest(BaseModel):
    """Schema for bulk deactivate request."""

    ids: list[int]


class BulkDesactivarResponse(BaseModel):
    """Schema for bulk deactivate response."""

    message: str
    desactivados: list[int]
    no_encontrados: list[int]
    total_desactivados: int
=======

class PoblarRequest(BaseModel):
    """Schema for bulk populate request."""
    cantidad: int


class PoblarResponse(BaseModel):
    """Schema for bulk populate response."""
    message: str
    status: int


class ResetResponse(BaseModel):
    """Schema for reset response."""
    message: str
    deleted_count: int