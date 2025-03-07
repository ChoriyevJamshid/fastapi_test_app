__all__ = (
    "settings",
    "db",
    "User",
    "Patient",
    "Hospitalization",
    "MedicalRecords"
)

from .config import settings
from .db_connector import db
from .models import User, Patient, Hospitalization, MedicalRecords
