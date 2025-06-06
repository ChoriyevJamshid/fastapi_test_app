from datetime import datetime

from sqlalchemy import ForeignKey, func, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class MedicalRecords(Base):
    __tablename__ = "medical_records"

    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), unique=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, server_default=func.now())
    diagnosis: Mapped[str] = mapped_column(Text)
    treatment: Mapped[str] = mapped_column(Text)

    # __table_args__ = (
    #     UniqueConstraint("patient_id", "doctor_id"),
    # )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"

