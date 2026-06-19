# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# TEST: HEALTH ROUTE
# FILE: tests/test_health.py
# ============================================================

from fastapi.testclient import TestClient

from app.api.main import app


# ============================================================
# SECTION 01 - HEALTH ROUTE TEST
# ============================================================

def test_health_route():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] in [
        "healthy",
        "degraded",
    ]

    assert "database" in payload
    assert "service" in payload
    assert payload["service"] == "aisp-baseball-api"