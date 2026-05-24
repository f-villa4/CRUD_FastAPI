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

def estadisticas_edad(db: Session) -> dict[str, Any]:
    """Return average, min and max age from birth_date."""

    edad = func.timestampdiff(
        literal_column("YEAR"),
        Persona.birth_date,
        func.curdate(),
    )

    row = (
        db.query(
            func.avg(edad).label("promedio"),
            func.min(edad).label("minima"),
            func.max(edad).label("maxima"),
        )
        .filter(Persona.birth_date.isnot(None))
        .one()
    )

    if row.promedio is None:
        return {
            "edad_promedio": 0,
            "edad_minima": 0,
            "edad_maxima": 0,
        }
    
    return {
        "edad_promedio": int(round(float(row.promedio))),
        "edad_minima": int(row.minima),
        "edad_maxima": int(row.maxima),
    }

def cumpleanios_por_mes(db: Session, numero_mes: int):
    """Return Personas with birthday in the given month."""

    return (
        db.query(Persona)
        .filter(
            Persona.birth_date.isnot(None),
            extract("month", Persona.birth_date) == numero_mes,
        )
        .all()
    )
