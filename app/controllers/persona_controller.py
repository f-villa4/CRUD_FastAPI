from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db

from ..views.persona import (
    PersonaCreate,
    PersonaLabRead,
    PersonaRead,
    PersonaUpdate,
)

from ..services import persona_analitica_fechas
from ..services import persona_service


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

#analítica SQL y filtros por fecha

@router.get("/estadisticas/dominios")
def estadisticas_dominios(db: Session = Depends(get_db)) -> dict[str, int]:
    """Count Personas per email domain."""
    return persona_analitica_fechas.estadisticas_dominios(db)

@router.get("/estadisticas/edad")
def estadisticas_edad(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Average, min and max age from birth_date."""
    return persona_analitica_fechas.estadisticas_edad(db)


@router.get(
    "/cumpleanios/mes/{numero_mes}",
    response_model=List[PersonaLabRead]
)
def cumpleanios_mes(
    numero_mes: int,
    db: Session = Depends(get_db)
):
    """Personas with birthday in the given month (1-12)."""

    if numero_mes < 1 or numero_mes > 12:
        raise HTTPException(
            status_code=400,
            detail="El mes debe ser un entero entre 1 y 12.",
        )

    return persona_analitica_fechas.cumpleanios_por_mes(
        db,
        numero_mes
    )


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
