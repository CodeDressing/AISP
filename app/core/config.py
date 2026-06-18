# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 3.30 PART 1
# ENTERPRISE APPLICATION CONFIGURATION EXPANSION
# FILE: app/core/config.py
# PURPOSE: centralized configuration for application identity,
# databases, MLB data sources, AI services, predictions,
# dashboards, deployment, security, logging, and future expansion
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
    # APPLICATION IDENTITY
    # --------------------------------------------------------

    app_name: str = "AISP Baseball Analytics Engine"
    app_short_name: str = "AISP"
    app_version: str = "1.0.0"
    app_description: str = (
        "Artificial Intelligence Sports Predictor for MLB "
        "analytics, rosters, statistics, predictions, and AI chat."
    )

    environment: str = "development"
    debug: bool = True

    # --------------------------------------------------------
    # API SETTINGS
    # --------------------------------------------------------

    api_title: str = "AISP Baseball API"
    api_prefix: str = ""
    api_docs_enabled: bool = True

    allowed_origins: str = "*"

    # --------------------------------------------------------
    # DATABASE SETTINGS
    # --------------------------------------------------------

    database_url: str = (
        "sqlite:///./data/warehouse/aisp_baseball.db"
    )

    postgres_url: str = ""
    duckdb_path: str = "./warehouse/analytics.duckdb"

    database_echo: bool = False
    database_pool_pre_ping: bool = True

    # --------------------------------------------------------
    # LOCAL STORAGE PATHS
    # --------------------------------------------------------

    data_root: str = "./data"
    raw_data_path: str = "./data/raw"
    processed_data_path: str = "./data/processed"
    warehouse_data_path: str = "./data/warehouse"
    model_data_path: str = "./data/models"

    # --------------------------------------------------------
    # MLB DATA SOURCES
    # --------------------------------------------------------

    mlb_api_base_url: str = (
        "https://statsapi.mlb.com/api/v1"
    )

    mlb_default_season: int = 2026
    mlb_sport_id: int = 1

    baseball_savant_enabled: bool = True
    fangraphs_enabled: bool = False
    retrosheet_enabled: bool = False
    lahman_enabled: bool = False

    # --------------------------------------------------------
    # MLB INGESTION SETTINGS
    # --------------------------------------------------------

    roster_sync_enabled: bool = True
    player_sync_enabled: bool = True
    team_sync_enabled: bool = True
    player_stats_sync_enabled: bool = True
    game_sync_enabled: bool = False
    transaction_sync_enabled: bool = False
    injury_sync_enabled: bool = False
    statcast_sync_enabled: bool = False

    roster_types: str = "active,40Man"

    # --------------------------------------------------------
    # AI CONFIGURATION
    # --------------------------------------------------------

    openai_api_key: str = ""

    chatbot_model: str = "gpt-5"
    embedding_model: str = "text-embedding-3-large"

    ai_chat_enabled: bool = True
    ai_database_lookup_enabled: bool = True
    ai_prediction_routing_enabled: bool = True
    ai_explanations_enabled: bool = True

    # --------------------------------------------------------
    # VECTOR SEARCH
    # --------------------------------------------------------

    vector_store_enabled: bool = False
    vector_store_provider: str = "local"

    vector_store_path: str = (
        "./data/vector_store"
    )

    # --------------------------------------------------------
    # PREDICTION ENGINE
    # --------------------------------------------------------

    prediction_engine_enabled: bool = True

    default_prediction_model: str = (
        "baseline"
    )

    advanced_prediction_model_enabled: bool = False
    monte_carlo_enabled: bool = False
    simulation_count: int = 10000

    minimum_prediction_confidence: float = 0.50
    home_field_advantage: float = 0.035

    # --------------------------------------------------------
    # BACKTESTING
    # --------------------------------------------------------

    backtesting_enabled: bool = True
    backtesting_default_start_year: int = 2021
    backtesting_default_end_year: int = 2026

    # --------------------------------------------------------
    # DASHBOARD SETTINGS
    # --------------------------------------------------------

    dashboard_enabled: bool = True
    dashboard_title: str = "AISP Baseball Analytics"
    dashboard_theme: str = "dark"

    dashboard_api_base_url: str = (
        "http://127.0.0.1:8000"
    )

    # --------------------------------------------------------
    # CACHE SETTINGS
    # --------------------------------------------------------

    cache_enabled: bool = False
    redis_url: str = ""
    cache_ttl_seconds: int = 300

    # --------------------------------------------------------
    # SECURITY SETTINGS
    # --------------------------------------------------------

    api_key_required: bool = False
    api_key_header_name: str = "X-AISP-API-Key"

    secret_key: str = (
        "CHANGE_THIS_IN_PRODUCTION"
    )

    admin_mode_enabled: bool = False

    # --------------------------------------------------------
    # LOGGING SETTINGS
    # --------------------------------------------------------

    log_level: str = "INFO"
    log_requests: bool = True
    log_predictions: bool = True
    log_ingestion_jobs: bool = True

    # --------------------------------------------------------
    # DEPLOYMENT SETTINGS
    # --------------------------------------------------------

    render_environment: bool = False
    render_service_name: str = "aisp-baseball-api"

    public_base_url: str = ""
    github_repo_url: str = "https://github.com/CodeDressing/AISP"

    # --------------------------------------------------------
    # FUTURE MULTI-SPORT SETTINGS
    # --------------------------------------------------------

    mlb_enabled: bool = True
    nfl_enabled: bool = False
    nba_enabled: bool = False
    nhl_enabled: bool = False
    soccer_enabled: bool = False
    esports_enabled: bool = False

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
    "player_profiles": True,
    "player_stats": True,
    "team_stats": True,
    "games": False,
    "game_logs": False,
    "statcast": False,
    "injuries": False,
    "transactions": False,
    "predictions": True,
    "advanced_predictions": False,
    "monte_carlo": False,
    "ai_chat": True,
    "database_aware_chat": True,
    "backtesting": True,
    "dashboard": True,
    "sportsbook_intelligence": False,
}


# ============================================================
# SECTION 05 - ENVIRONMENT HELPERS
# ============================================================

def is_production() -> bool:
    return settings.environment.lower() == "production"


def is_development() -> bool:
    return settings.environment.lower() == "development"


def is_render() -> bool:
    return settings.render_environment


# ============================================================
# SECTION 06 - MLB HELPER SETTINGS
# ============================================================

def get_roster_type_list() -> list[str]:
    return [
        item.strip()
        for item in settings.roster_types.split(",")
        if item.strip()
    ]


# ============================================================
# SECTION 07 - APPLICATION METADATA
# ============================================================

def get_application_metadata() -> dict:
    return {
        "app_name": settings.app_name,
        "short_name": settings.app_short_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "render": settings.render_environment,
        "github": settings.github_repo_url,
    }


# ============================================================
# SECTION 08 - FUTURE SPORTS ROADMAP
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
Live Betting
Sportsbook Edge Detection

Platform Targets

FastAPI Backend
Streamlit Dashboard
React / Next.js Frontend
PostgreSQL Production Database
DuckDB Analytics Warehouse
Vector Search Layer
AI Chatbot
Machine Learning Model Store
Backtesting Engine
Render Deployment
GitHub CI/CD
"""