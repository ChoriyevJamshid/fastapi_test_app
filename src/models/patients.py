import enum
from datetime import date

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class StatusEnum(enum.Enum):
    registered = "registered"
    hospitalized = "hospitalized"
    discharged = "discharged"


class Patient(Base):
    __tablename__ = "patients"

    full_name: Mapped[str]
    birth_date: Mapped[date] = mapped_column()
    gender: Mapped[str] = mapped_column(Enum(GenderEnum))
    contact_info: Mapped[str]
    status: Mapped[str] = mapped_column(Enum(StatusEnum))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id}, full_name = {self.full_name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id}, full_name = {self.full_name})"
