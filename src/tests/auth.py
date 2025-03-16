from fastapi.testclient import TestClient
from fastapi import status

from src.app import app
from src.models.users import RoleEnum

client = TestClient(app)

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3NDIxMzg0NDIsImlhdCI6MTc0MjEzNDg0Mn0.1VpJSr0MLPD4QGLmQjngHyD_pG4N8TP1W2pc3-ahVLc'
URL = "api/v1/auth"


def test_auth_register():
    params = {
        "email": "",
        "role": RoleEnum.patient.value,
        "password": "",
        "active": True
    }
    response = client.post(
        f"{URL}/register",
        params=params,
        headers={
            "Authorization": f"Bearer {TOKEN}"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_auth_login():
    params = {
        "email": "",
        "password": ""
    }
    response = client.post(
        f"{URL}/login",
        params=params,
        headers={
            "Authorization": f"Bearer {TOKEN}"
        }
    )

    assert response.status_code == status.HTTP_200_OK

def test_auth_me():
    response = client.get(
        f"{URL}/me",
        headers={
            "Authorization": f"Bearer {TOKEN}"
        }
    )
    assert response.status_code == status.HTTP_200_OK



