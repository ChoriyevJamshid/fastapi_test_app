import enum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class RoleEnum(enum.Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"
    patient = "patient"


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(Enum(RoleEnum))
    active: Mapped[bool] = mapped_column(default=True, server_default="true")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id}, email = {self.email})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id}, email = {self.email})"
