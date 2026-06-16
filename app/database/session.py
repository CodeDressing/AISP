# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 1.03 PART 1
# ENTERPRISE DATABASE INFRASTRUCTURE
# FILE: app/database/session.py
# PURPOSE: centralized database engine, session management,
#           dependency injection, and future warehouse support
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# ============================================================
# SECTION 02 - DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = settings.database_url

IS_SQLITE = DATABASE_URL.startswith("sqlite")


# ============================================================
# SECTION 03 - DATABASE ENGINE CONFIGURATION
# ============================================================

ENGINE_OPTIONS = {
    "pool_pre_ping": True,
}

if IS_SQLITE:
    ENGINE_OPTIONS["connect_args"] = {
        "check_same_thread": False,
    }


# ============================================================
# SECTION 04 - PRIMARY DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    **ENGINE_OPTIONS,
)


# ============================================================
# SECTION 05 - SESSION FACTORY
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ============================================================
# SECTION 06 - DECLARATIVE BASE
# ============================================================

Base = declarative_base()


# ============================================================
# SECTION 07 - API DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    FastAPI dependency injection helper.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# SECTION 08 - DIRECT SESSION HELPER
# ============================================================

def create_session():
    """
    Direct session creation helper for
    scripts, ETL jobs, analytics jobs,
    prediction jobs, and background workers.
    """

    return SessionLocal()


# ============================================================
# SECTION 09 - HEALTH CHECK UTILITIES
# ============================================================

def database_health_check() -> bool:
    """
    Verify database connectivity.
    """

    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()

        return True

    except Exception:
        return False


# ============================================================
# SECTION 10 - FUTURE WAREHOUSE PLACEHOLDERS
# ============================================================

"""
Future Database Targets

SQLite:
    Development

PostgreSQL:
    Production

DuckDB:
    Analytics Warehouse

Redis:
    Caching Layer

Vector Database:
    AI Search Layer
"""