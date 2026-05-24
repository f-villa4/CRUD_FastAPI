from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import (
    persona_analitica_fechas,
    persona_busqueda_bulk,
    persona_masivas,
    persona_service,
)
from ..views.persona import (
    BulkDesactivarRequest,
    BulkDesactivarResponse,
    PersonaActivaReport,
    PersonaCreate,
    PersonaLabRead,
    PersonaRead,
    PersonaUpdate,
    PoblarRequest,
    PoblarResponse,
    ResetResponse,
)

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

@router.patch("/bulk/desactivar", response_model=BulkDesactivarResponse)
def bulk_desactivar(body: BulkDesactivarRequest, db: Session = Depends(get_db)):
    """Deactivate multiple Personas by ID."""
    if not body.ids or len(body.ids) > 100:
        raise HTTPException(
            status_code=400,
            detail="La lista de ids debe tener entre 1 y 100 elementos.",
        )

    result = persona_busqueda_bulk.bulk_desactivar(db, body.ids)
    return BulkDesactivarResponse(**result)
    
  
@router.get("/estadisticas/dominios")
def estadisticas_dominios(db: Session = Depends(get_db)) -> dict[str, int]:
    """Count Personas per email domain."""
    return persona_analitica_fechas.estadisticas_dominios(db)

    
@router.get("/estadisticas/edad")
def estadisticas_edad(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Average, min and max age from birth_date."""
    return persona_analitica_fechas.estadisticas_edad(db)


@router.get("/cumpleanios/mes/{numero_mes}", response_model=List[PersonaLabRead])
def cumpleanios_mes(numero_mes: int, db: Session = Depends(get_db)):
    """Personas with birthday in the given month (1-12)."""
    if numero_mes < 1 or numero_mes > 12:
        raise HTTPException(
            status_code=400,
            detail="El mes debe ser un entero entre 1 y 12.",
        )
    return persona_analitica_fechas.cumpleanios_por_mes(db, numero_mes)

  
@router.post("/poblar", response_model=PoblarResponse, status_code=status.HTTP_201_CREATED)
def poblar_personas(body: PoblarRequest, db: Session = Depends(get_db)):
    """Bulk insert Personas using Faker."""
    if body.cantidad <= 0 or body.cantidad > 1000:
        raise HTTPException(
            status_code=400,
            detail="cantidad debe estar entre 1 y 1000",
        )
    n = persona_masivas.poblar_personas(db, body.cantidad)
    return PoblarResponse(
        message=f"{n} usuarios creados exitosamente",
        status=201,
    )
    
    
@router.delete("/reset", response_model=ResetResponse)
def reset_personas(db: Session = Depends(get_db)):
    """Delete all Personas from the table."""
    deleted_count = persona_masivas.reset_all_personas(db)
    return ResetResponse(
        message="Base de datos limpiada. Se eliminaron todos los registros.",
        deleted_count=deleted_count,
    )
  

@router.get("/exportar/csv")
def exportar_csv(db: Session = Depends(get_db)):
    """Export all Personas as CSV download."""
    content = persona_masivas.exportar_personas_csv(db)
    return StreamingResponse(
        persona_masivas.iter_csv_content(content),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="personas.csv"'},
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
