from datetime import date

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base

class Hospitalization(Base):
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), unique=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admission_date: Mapped[date] = mapped_column()
    discharge_date: Mapped[date | None]


    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"

