import csv
import io
import random
import re
from datetime import date

from faker import Faker
from sqlalchemy.orm import Session

from ..models.persona import Persona

_fake = Faker("es_ES")
_DOMINIOS = ("gmail.com", "outlook.com", "hotmail.com", "yahoo.com")

_CSV_HEADER = (
    "id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "birth_date",
    "is_active",
    "notes",
)


def _slug(text: str) -> str:
    normalized = text.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "", normalized)
    return normalized or "usuario"


def _build_unique_email(
    db: Session,
    first_name: str,
    last_name: str,
    existing: set[str],
) -> str:
    base_local = f"{_slug(first_name)}.{_slug(last_name)}"
    domain = random.choice(_DOMINIOS)
    candidate = f"{base_local}@{domain}"
    suffix = 1
    while candidate in existing or db.query(Persona.id).filter(Persona.email == candidate).first():
        candidate = f"{base_local}{suffix}@{domain}"
        suffix += 1
    existing.add(candidate)
    return candidate


def _build_persona(db: Session, existing_emails: set[str]) -> Persona:
    first_name = _fake.first_name()
    last_name = _fake.last_name()
    email = _build_unique_email(db, first_name, last_name, existing_emails)
    notes = _fake.sentence(nb_words=6) if random.random() < 0.7 else None
    return Persona(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=_fake.phone_number()[:30],
        birth_date=_fake.date_of_birth(minimum_age=18, maximum_age=85),
        is_active=bool(random.getrandbits(1)),
        notes=notes,
    )
    
    
def poblar_personas(db: Session, cantidad: int) -> int:
    """Insert cantidad Personas generated with Faker."""
    existing_emails: set[str] = set()
    batch = [_build_persona(db, existing_emails) for _ in range(cantidad)]
    db.add_all(batch)
    db.commit()
    return cantidad


def reset_all_personas(db: Session) -> int:
    """Delete all rows and return deleted count."""
    deleted_count = db.query(Persona).delete()
    db.commit()
    return deleted_count

