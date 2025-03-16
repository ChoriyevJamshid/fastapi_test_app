from fastapi.testclient import TestClient
from fastapi import status

from src.app import app
from src.models.users import RoleEnum

client = TestClient(app)

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3NDIxMzg0NDIsImlhdCI6MTc0MjEzNDg0Mn0.1VpJSr0MLPD4QGLmQjngHyD_pG4N8TP1W2pc3-ahVLc'

def test_update_user():
    user_id: int = 2
    response = client.put(
        f"/api/v1/users/{user_id}/",
        params={
            "email": "",
            "role": RoleEnum.admin.value,
            "active": True
        },
        headers={
            "Authorization": f"Bearer {TOKEN}",
        },
    )
    assert response.status_code == status.HTTP_200_OK

def test_delete_user():
    user_id: int = 2
    response = client.delete(
        f"/api/v1/users/{user_id}/",
        headers={
            "Authorization": f"Bearer {TOKEN}",
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT



