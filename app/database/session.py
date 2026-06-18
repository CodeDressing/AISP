# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 3.31 PART 1
# ENTERPRISE DATABASE SESSION INFRASTRUCTURE
# FILE: app/database/session.py
# PURPOSE: centralized database engine, session management,
# FastAPI dependency injection, health checks, and future
# warehouse/database expansion support
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# ============================================================
# SECTION 02 - DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = settings.database_url

IS_SQLITE = DATABASE_URL.startswith("sqlite")


# ============================================================
# SECTION 03 - DATABASE ENGINE OPTIONS
# ============================================================

ENGINE_OPTIONS = {
    "pool_pre_ping": settings.database_pool_pre_ping,
    "echo": settings.database_echo,
}

if IS_SQLITE:
    ENGINE_OPTIONS["connect_args"] = {
        "check_same_thread": False,
    }


# ============================================================
# SECTION 04 - PRIMARY DATABASE ENGINE
# ============================================================

engine: Engine = create_engine(
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
# SECTION 07 - FASTAPI DATABASE DEPENDENCY
# ============================================================

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# SECTION 08 - DIRECT SESSION HELPER
# ============================================================

def create_session() -> Session:
    return SessionLocal()


# ============================================================
# SECTION 09 - CONTEXT MANAGER SESSION HELPER
# ============================================================

@contextmanager
def managed_session() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


# ============================================================
# SECTION 10 - DATABASE HEALTH CHECK
# ============================================================

def database_health_check() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(
                text("SELECT 1")
            )

        return True

    except Exception:
        return False


# ============================================================
# SECTION 11 - DATABASE HEALTH DETAILS
# ============================================================

def database_health_details() -> dict:
    return {
        "database_url_configured": bool(DATABASE_URL),
        "database_type": "sqlite" if IS_SQLITE else "external",
        "connection_ok": database_health_check(),
        "pool_pre_ping": settings.database_pool_pre_ping,
        "echo": settings.database_echo,
    }


# ============================================================
# SECTION 12 - DATABASE INITIALIZATION HELPER
# ============================================================

def initialize_database() -> None:
    Base.metadata.create_all(
        bind=engine,
    )


# ============================================================
# SECTION 13 - FUTURE DATABASE ROADMAP
# ============================================================

"""
Future Database Targets

SQLite:
    Local development

PostgreSQL:
    Render production database

DuckDB:
    Analytics warehouse

Redis:
    Caching and job state

Vector Database:
    AI search and player/team context retrieval
"""