# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 1.03 PART 2
# ENTERPRISE APPLICATION CONFIGURATION
# FILE: app/core/config.py
# PURPOSE: centralized configuration management for
# MLB analytics, AI services, databases, deployment,
# machine learning, and future sportsbook expansion
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


# ============================================================
# SECTION 02 - APPLICATION SETTINGS
# ============================================================

class Settings(BaseSettings):

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    app_name: str = "AISP Baseball Analytics Engine"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # --------------------------------------------------------
    # DATABASES
    # --------------------------------------------------------

    database_url: str = (
        "sqlite:///./data/warehouse/aisp_baseball.db"
    )

    postgres_url: str = ""
    duckdb_path: str = "./warehouse/analytics.duckdb"

    # --------------------------------------------------------
    # MLB DATA SOURCES
    # --------------------------------------------------------

    mlb_api_base_url: str = (
        "https://statsapi.mlb.com/api/v1"
    )

    baseball_savant_enabled: bool = True
    fangraphs_enabled: bool = False
    retrosheet_enabled: bool = False

    # --------------------------------------------------------
    # AI CONFIGURATION
    # --------------------------------------------------------

    openai_api_key: str = ""

    chatbot_model: str = "gpt-5"
    embedding_model: str = "text-embedding-3-large"

    ai_chat_enabled: bool = True

    # --------------------------------------------------------
    # VECTOR SEARCH
    # --------------------------------------------------------

    vector_store_enabled: bool = False

    vector_store_path: str = (
        "./data/vector_store"
    )

    # --------------------------------------------------------
    # PREDICTION ENGINE
    # --------------------------------------------------------

    prediction_engine_enabled: bool = True

    default_prediction_model: str = (
        "xgboost"
    )

    simulation_count: int = 10000

    # --------------------------------------------------------
    # BACKTESTING
    # --------------------------------------------------------

    backtesting_enabled: bool = True

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    redis_url: str = ""

    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------

    api_key_required: bool = False

    secret_key: str = (
        "CHANGE_THIS_IN_PRODUCTION"
    )

    # --------------------------------------------------------
    # DEPLOYMENT
    # --------------------------------------------------------

    render_environment: bool = False

    # --------------------------------------------------------
    # PYDANTIC SETTINGS CONFIG
    # --------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# ============================================================
# SECTION 03 - SETTINGS SINGLETON
# ============================================================

settings = Settings()


# ============================================================
# SECTION 04 - FEATURE FLAGS
# ============================================================

FEATURES = {
    "mlb_rosters": True,
    "player_stats": True,
    "team_stats": True,
    "statcast": False,
    "injuries": False,
    "transactions": False,
    "predictions": True,
    "ai_chat": True,
    "backtesting": True,
}


# ============================================================
# SECTION 05 - FUTURE SPORTS ROADMAP
# ============================================================

"""
AISP Expansion Targets

MLB
NFL
NBA
NHL
MLS
EPL
NCAA
Esports

Prediction Markets

Moneyline
Spread
Totals
Player Props
Fantasy Sports
DFS
Simulation Models
"""