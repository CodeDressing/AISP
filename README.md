# AISP Baseball Analytics Engine

Python 3.14-ready enterprise starter project for MLB roster ingestion, player statistics, prediction services, and an AI chatbot interface.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/build_master_database.py
uvicorn app.api.main:app --reload
```

Dashboard:

```bash
streamlit run apps/dashboard/dashboard.py
```

## Project Goal

AISP is designed to become a larger Artificial Intelligence Sports Predictor platform. This first module focuses on MLB data, rosters, player stats, and prediction scaffolding.
