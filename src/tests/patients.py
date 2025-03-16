from fastapi.params import Depends
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app import app
from src.db import connector

client = TestClient(app)


def test_get_patient():
    response = client.get("/api/v1/patients/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND





