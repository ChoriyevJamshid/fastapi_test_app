from fastapi.testclient import TestClient
from fastapi import status

from src.app import app

client = TestClient(app)

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3NDIxMzg0NDIsImlhdCI6MTc0MjEzNDg0Mn0.1VpJSr0MLPD4QGLmQjngHyD_pG4N8TP1W2pc3-ahVLc'
URL = "api/v1/medical_records"

def test_get_medical_record():
    patient_id: int = 1
    response = client.get(
        f"{URL}/{patient_id}",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_create_medical_record():
    patient_id: int = 1
    params = {
        "created_at": "",
        "diagnosis": "",
        "treatment": "",
        "doctor_id": 1
    }

    response = client.post(
        f"{URL}/{patient_id}",
        headers={"Authorization": f"Bearer {TOKEN}"},
        params=params
    )
    assert response.status_code == status.HTTP_201_CREATED

def test_update_medical_record():
    patient_id: int = 1
    params = {
        "created_at": "",
        "diagnosis": "",
        "treatment": "",
        "doctor_id": 1
    }

    response = client.put(
        f"{URL}/{patient_id}",
        headers={"Authorization": f"Bearer {TOKEN}"},
        params=params
    )
    assert response.status_code == status.HTTP_200_OK


def test_delete_medical_record():
    patient_id: int = 1
    response = client.delete(
        f"{URL}/{patient_id}",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

