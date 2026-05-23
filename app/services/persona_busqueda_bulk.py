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