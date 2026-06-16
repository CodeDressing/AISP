# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 1.07 PART 1
# ENTERPRISE RENDER DEPLOYMENT
# FILE: render.yaml
# PURPOSE: production deployment configuration
# ============================================================

services:

  # ==========================================================
  # SECTION 01 - FASTAPI WEB SERVICE
  # ==========================================================

  - type: web

    name: aisp-baseball-api

    runtime: python

    plan: free

    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt

    startCommand: |
      uvicorn app.api.main:app --host 0.0.0.0 --port $PORT

    healthCheckPath: /health

    envVars:

      - key: ENVIRONMENT
        value: production

      - key: RENDER_ENVIRONMENT
        value: "True"

      - key: PYTHON_VERSION
        value: "3.14"

      - key: DATABASE_URL
        value: sqlite:///./data/warehouse/aisp_baseball.db

      - key: MLB_API_BASE_URL
        value: https://statsapi.mlb.com/api/v1