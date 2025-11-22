from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_sign_in():
    response = client.post("/auth/signIn", json={"email": "example@example.com", "password": "1234"})
    assert response.status_code == 200
    assert response.json() == {"access_token": "example_token"}