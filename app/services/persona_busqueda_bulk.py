from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.persona import Persona

def buscar_personas(db: Session, termino: str):
    """Search term in first_name, last_name or email (OR)."""

    pattern = f"%{termino}%"

    return (
        db.query(Persona)
        .filter(
            or_(
                Persona.first_name.like(pattern),
                Persona.last_name.like(pattern),
                Persona.email.like(pattern),
            )
        )
        .all()
    )

def reporte_activos(db: Session):
    """Return active Personas."""

    return (
        db.query(Persona)
        .filter(Persona.is_active.is_(True))
        .all()
    )

def bulk_desactivar(db: Session, ids: list[int]) -> dict:
    """Set is_active=False for existing ids; report missing ids."""

    unique_ids = list(dict.fromkeys(ids))

    found = (
        db.query(Persona)
        .filter(Persona.id.in_(unique_ids))
        .all()
    )

    found_ids = {p.id for p in found}

    desactivados = sorted(found_ids)

    no_encontrados = sorted(
        i for i in unique_ids if i not in found_ids
    )

    for persona in found:
        persona.is_active = False

    db.commit()

    return {
        "message": "Operación completada.",
        "desactivados": desactivados,
        "no_encontrados": no_encontrados,
        "total_desactivados": len(desactivados),
    }