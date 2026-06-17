# AISP Baseball Project Structure



# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 2.00 PART 2
# ENTERPRISE PROJECT STRUCTURE MAP
# FILE: docs/PROJECT_STRUCTURE.md
# PURPOSE: long-term scalable project structure for MLB analytics,
# prediction services, AI chatbot, Render deployment, and GitHub growth
# ============================================================

# AISP Baseball Project Structure

```text
AISP_Baseball_Python314/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── chatbot/
│   │   ├── __init__.py
│   │   └── router.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── data_sources/
│   │   ├── __init__.py
│   │   └── mlb_stats_api.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── session.py
│   │
│   ├── prediction/
│   │   ├── __init__.py
│   │   └── baseline_model.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── common.py
│   │
│   └── services/
│       ├── __init__.py
│       └── roster_service.py
│
├── analytics/
│   ├── batting/
│   │   └── .gitkeep
│   ├── pitching/
│   │   └── .gitkeep
│   ├── fielding/
│   │   └── .gitkeep
│   ├── statcast/
│   │   └── .gitkeep
│   └── sabermetrics/
│       └── .gitkeep
│
├── ai/
│   ├── chatbot/
│   │   └── .gitkeep
│   ├── prompts/
│   │   └── .gitkeep
│   ├── rag/
│   │   └── .gitkeep
│   ├── embeddings/
│   │   └── .gitkeep
│   └── vector_store/
│       └── .gitkeep
│
├── prediction_engine/
│   ├── game_models/
│   │   └── .gitkeep
│   ├── player_models/
│   │   └── .gitkeep
│   ├── betting_models/
│   │   └── .gitkeep
│   ├── simulations/
│   │   └── .gitkeep
│   └── backtesting/
│       └── .gitkeep
│
├── apps/
│   ├── dashboard/
│   │   └── dashboard.py
│   └── worker/
│       └── .gitkeep
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   ├── warehouse/
│   │   └── .gitkeep
│   └── models/
│       └── .gitkeep
│
├── warehouse/
│   ├── bronze/
│   │   └── .gitkeep
│   ├── silver/
│   │   └── .gitkeep
│   ├── gold/
│   │   └── .gitkeep
│   └── exports/
│       └── .gitkeep
│
├── ml_models/
│   ├── xgboost/
│   │   └── .gitkeep
│   ├── lightgbm/
│   │   └── .gitkeep
│   ├── random_forest/
│   │   └── .gitkeep
│   └── ensembles/
│       └── .gitkeep
│
├── monitoring/
│   ├── logs/
│   │   └── .gitkeep
│   ├── health/
│   │   └── .gitkeep
│   └── performance/
│       └── .gitkeep
│
├── deployments/
│   ├── render/
│   │   └── .gitkeep
│   └── github_actions/
│       └── .gitkeep
│
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   ├── API_ROUTES.md
│   ├── DATA_SOURCES.md
│   ├── DEPLOYMENT_RENDER.md
│   └── ROADMAP.md
│
├── scripts/
│   └── build_master_database.py
│
├── tests/
│   └── test_health.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
├── render.yaml
└── requirements.txt

```text
AISP_Baseball_Python314/
├── app/
│   ├── api/
│   ├── chatbot/
│   ├── core/
│   ├── data_sources/
│   ├── database/
│   ├── prediction/
│   ├── schemas/
│   └── services/
├── apps/
│   ├── dashboard/
│   └── worker/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── warehouse/
│   └── models/
├── scripts/
├── tests/
├── docs/
├── .github/workflows/
├── render.yaml
├── requirements.txt
├── pyproject.toml
└── README.md
```
