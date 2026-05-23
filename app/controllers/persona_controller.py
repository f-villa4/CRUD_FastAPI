from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..views.persona import (
    PersonaActivaReport,
    BulkDesactivarRequest,
    BulkDesactivarResponse,
    PersonaCreate,
    PersonaLabRead,
    PersonaRead,
    PersonaUpdate,
)
from ..services import persona_service, persona_busqueda_bulk

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post("", response_model=PersonaRead, status_code=status.HTTP_201_CREATED)
def create_persona(persona_in: PersonaCreate, db: Session = Depends(get_db)):
    """Create a new Persona delegating to service layer."""
    # Let domain errors bubble up to global handlers
    return persona_service.create_persona(db, persona_in)


@router.get("", response_model=List[PersonaRead])
def list_personas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List Personas with pagination via service layer."""
    return persona_service.list_personas(db, skip=skip, limit=limit)

@router.get("/buscar/{termino}", response_model=List[PersonaLabRead])
def buscar_personas(termino: str, db: Session = Depends(get_db)):
    """Search term in first_name, last_name or email."""

    return persona_busqueda_bulk.buscar_personas(db, termino)

@router.get("/reporte/activos", response_model=List[PersonaActivaReport])
def reporte_activos(db: Session = Depends(get_db)):
    """List active Personas with projected fields."""

    return persona_busqueda_bulk.reporte_activos(db)


@router.get("/{persona_id}", response_model=PersonaRead)
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    """Retrieve a Persona by ID via service layer."""
    return persona_service.get_persona(db, persona_id)


@router.put("/{persona_id}", response_model=PersonaRead)
def update_persona(persona_id: int, persona_in: PersonaUpdate, db: Session = Depends(get_db)):
    """Update an existing Persona (partial) via service layer."""
    return persona_service.update_persona(db, persona_id, persona_in)


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    """Delete a Persona by ID via service layer."""
    persona_service.delete_persona(db, persona_id)
    return None
