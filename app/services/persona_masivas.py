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