# SECTION 1: Imports
from fastapi.testclient import TestClient

from app.api.main import app


# SECTION 2: Health Test
def test_health_route():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
