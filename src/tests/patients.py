from fastapi.testclient import TestClient
from fastapi import status

from src.app import app

client = TestClient(app)


def test_get_patient():
    response = client.get("/api/v1/patients/1")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK


def test_create_patient():
    response = client.post(
        "/api/v1/patients",
        params={
            "full_name": "New patient 1",
            "birth_date": "2000-01-01",
            "gender": "male",
            "contact_info": "Contact info",
            "status": "registered",
        },
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3NDIxMzg0NDIsImlhdCI6MTc0MjEzNDg0Mn0.1VpJSr0MLPD4QGLmQjngHyD_pG4N8TP1W2pc3-ahVLc",
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_update_patient():
    patient_id: int = 1
    response = client.put(
        f"/api/v1/patients/{patient_id}",
        params={
            "full_name": "New patient 1",
            "birth_date": "2000-01-01",
            "gender": "female",
            "contact_info": "Contact info updated",
            "status": "registered",
        },
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3NDIxMzg0NDIsImlhdCI6MTc0MjEzNDg0Mn0.1VpJSr0MLPD4QGLmQjngHyD_pG4N8TP1W2pc3-ahVLc",
        }
    )

    assert response.status_code == status.HTTP_200_OK


def test_delete_patient():
    patient_id: int = 1
    response = client.delete(
        f"/api/v1/patients/{patient_id}",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3NDIxMzg0NDIsImlhdCI6MTc0MjEzNDg0Mn0.1VpJSr0MLPD4QGLmQjngHyD_pG4N8TP1W2pc3-ahVLc",
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
