import enum
import asyncio
from datetime import datetime, date

from sqlalchemy import (
    Enum,
    ForeignKey,
    Text,
    func
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column
)


class RoleEnum(enum.Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"
    patient = "patient"


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class StatusEnum(enum.Enum):
    registered = "registered"
    hospitalized = "hospitalized"
    discharged = "discharged"


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


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


class Hospitalization(Base):
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admission_date: Mapped[date] = mapped_column()
    discharge_date: Mapped[date | None]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"


class MedicalRecords(Base):
    __tablename__ = "medical_records"

    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, server_default=func.now())
    diagnosis: Mapped[str] = mapped_column(Text)
    treatment: Mapped[str] = mapped_column(Text)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id = {self.id})"


async def main():
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///test.sqlite3",
        echo=True,
    )
    async_session = async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    print(Base.metadata.tables.keys())
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())
