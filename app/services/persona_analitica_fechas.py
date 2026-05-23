from typing import Any
from sqlalchemy import extract, func, literal_column
from sqlalchemy.orm import Session
from ..models.persona import Persona

def estadisticas_dominios(db: Session) -> dict[str, int]:
    """Count Personas grouped by email domain."""
    dominio = func.substring_index(Persona.email, "@", -1)
    rows = (
        db.query(
            dominio.label("dominio"),
            func.count(Persona.id).label("cantidad")

        )
        .group_by(dominio)
        .all()
    )
    return {
        row.dominio: int(row.cantidad)
        for row in rows

    }