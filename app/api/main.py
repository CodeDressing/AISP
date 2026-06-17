# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 2.01 PART 1
# ENTERPRISE API GATEWAY UPGRADE
# FILE: app/api/main.py
# PURPOSE: Render-safe FastAPI gateway for health checks,
# teams, players, games, predictions, AI chat, and system info
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from pathlib import Path

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.chatbot.router import AISPChatbotRouter
from app.core.config import settings
from app.database.models import (
    Game,
    GamePrediction,
    Player,
    PlayerPrediction,
    Team,
)
from app.database.session import Base
from app.database.session import engine
from app.database.session import get_db
from app.schemas.common import ChatRequest


# ============================================================
# SECTION 02 - LOCAL STORAGE PREPARATION
# ============================================================

def prepare_local_storage() -> None:
    Path("data").mkdir(exist_ok=True)
    Path("data/warehouse").mkdir(parents=True, exist_ok=True)
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/processed").mkdir(parents=True, exist_ok=True)


prepare_local_storage()


# ============================================================
# SECTION 03 - DATABASE INITIALIZATION
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# SECTION 04 - APPLICATION INITIALIZATION
# ============================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AISP Baseball Analytics Engine API",
)

chatbot = AISPChatbotRouter()


# ============================================================
# SECTION 05 - CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SECTION 06 - DATABASE HEALTH CHECK
# ============================================================

def check_database_connection() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# ============================================================
# SECTION 07 - ROOT ROUTES
# ============================================================

@app.get("/")
def root() -> dict:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
        "platform": "AISP",
        "service": "aisp-baseball-api",
    }


# ============================================================
# SECTION 08 - HEALTH ROUTES
# ============================================================

@app.get("/health")
def health() -> dict:
    database_ok = check_database_connection()

    return {
        "status": "healthy" if database_ok else "degraded",
        "database": database_ok,
        "service": "aisp-baseball-api",
    }


@app.get("/health/database")
def database_health() -> dict:
    return {
        "database": check_database_connection(),
    }


# ============================================================
# SECTION 09 - TEAM ROUTES
# ============================================================

@app.get("/teams")
def get_teams(
    db: Session = Depends(get_db),
) -> list[dict]:
    teams = (
        db.query(Team)
        .order_by(Team.name)
        .all()
    )

    return [
        {
            "team_id": team.mlb_team_id,
            "name": team.name,
            "abbreviation": team.abbreviation,
            "league": team.league,
            "division": team.division,
            "venue": team.venue_name,
            "active": team.active,
        }
        for team in teams
    ]


@app.get("/teams/{team_id}")
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
) -> dict:
    team = (
        db.query(Team)
        .filter(Team.mlb_team_id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="team_not_found",
        )

    return {
        "team_id": team.mlb_team_id,
        "name": team.name,
        "abbreviation": team.abbreviation,
        "league": team.league,
        "division": team.division,
        "venue": team.venue_name,
        "active": team.active,
    }


# ============================================================
# SECTION 10 - PLAYER ROUTES
# ============================================================

@app.get("/players/search")
def search_players(
    q: str,
    db: Session = Depends(get_db),
) -> list[dict]:
    players = (
        db.query(Player)
        .filter(Player.full_name.ilike(f"%{q}%"))
        .order_by(Player.full_name)
        .limit(50)
        .all()
    )

    return [
        {
            "player_id": player.mlb_player_id,
            "name": player.full_name,
            "team": player.current_team_name,
            "position": player.position,
            "bats": player.bats,
            "throws": player.throws,
            "height": player.height,
            "weight": player.weight,
            "active": player.active,
        }
        for player in players
    ]


@app.get("/players/{player_id}")
def get_player(
    player_id: int,
    db: Session = Depends(get_db),
) -> dict:
    player = (
        db.query(Player)
        .filter(Player.mlb_player_id == player_id)
        .first()
    )

    if not player:
        raise HTTPException(
            status_code=404,
            detail="player_not_found",
        )

    return {
        "player_id": player.mlb_player_id,
        "name": player.full_name,
        "team_id": player.current_team_id,
        "team": player.current_team_name,
        "position": player.position,
        "bats": player.bats,
        "throws": player.throws,
        "height": player.height,
        "weight": player.weight,
        "birth_date": player.birth_date,
        "birth_city": player.birth_city,
        "birth_state": player.birth_state,
        "birth_country": player.birth_country,
        "mlb_debut_date": player.mlb_debut_date,
        "active": player.active,
    }


# ============================================================
# SECTION 11 - GAME ROUTES
# ============================================================

@app.get("/games")
def get_games(
    limit: int = 250,
    db: Session = Depends(get_db),
) -> list[dict]:
    safe_limit = min(max(limit, 1), 500)

    games = (
        db.query(Game)
        .order_by(Game.id.desc())
        .limit(safe_limit)
        .all()
    )

    return [
        {
            "game_pk": game.mlb_game_pk,
            "season": game.season,
            "date": game.game_date,
            "official_date": game.official_date,
            "home_team": game.home_team_name,
            "away_team": game.away_team_name,
            "home_score": game.home_score,
            "away_score": game.away_score,
            "status": game.status,
            "detailed_status": game.detailed_status,
            "venue": game.venue_name,
        }
        for game in games
    ]


# ============================================================
# SECTION 12 - GAME PREDICTION ROUTES
# ============================================================

@app.get("/predictions/games")
def get_game_predictions(
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[dict]:
    safe_limit = min(max(limit, 1), 250)

    rows = (
        db.query(GamePrediction)
        .order_by(GamePrediction.id.desc())
        .limit(safe_limit)
        .all()
    )

    return [
        {
            "game_pk": row.mlb_game_pk,
            "season": row.season,
            "home_team": row.home_team_name,
            "away_team": row.away_team_name,
            "predicted_home_score": row.predicted_home_score,
            "predicted_away_score": row.predicted_away_score,
            "predicted_winner": row.predicted_winner_team_name,
            "home_probability": row.home_win_probability,
            "away_probability": row.away_win_probability,
            "confidence": row.confidence,
            "model": row.model_name,
        }
        for row in rows
    ]


# ============================================================
# SECTION 13 - PLAYER PREDICTION ROUTES
# ============================================================

@app.get("/predictions/players")
def get_player_predictions(
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[dict]:
    safe_limit = min(max(limit, 1), 250)

    rows = (
        db.query(PlayerPrediction)
        .order_by(PlayerPrediction.id.desc())
        .limit(safe_limit)
        .all()
    )

    return [
        {
            "player_id": row.mlb_player_id,
            "player_name": row.player_name,
            "team": row.team_name,
            "market": row.prediction_market,
            "predicted_value": row.predicted_value,
            "probability_over": row.probability_over,
            "probability_under": row.probability_under,
            "confidence": row.confidence,
            "model": row.model_name,
        }
        for row in rows
    ]


# ============================================================
# SECTION 14 - AI CHAT ROUTES
# ============================================================

@app.post("/chat")
def chat(
    request: ChatRequest,
) -> dict:
    return chatbot.answer(
        request.message
    )


# ============================================================
# SECTION 15 - SYSTEM INFORMATION ROUTES
# ============================================================

@app.get("/system/info")
def system_info() -> dict:
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "prediction_engine": settings.prediction_engine_enabled,
        "ai_chat": settings.ai_chat_enabled,
        "database": check_database_connection(),
    }


@app.get("/system/routes")
def system_routes() -> dict:
    return {
        "routes": [
            "/",
            "/health",
            "/health/database",
            "/teams",
            "/teams/{team_id}",
            "/players/search?q=juan",
            "/players/{player_id}",
            "/games",
            "/predictions/games",
            "/predictions/players",
            "/chat",
            "/system/info",
            "/system/routes",
            "/docs",
        ]
    }


# ============================================================
# SECTION 16 - FUTURE API ROADMAP
# ============================================================

"""
Future Endpoints

/statcast
/injuries
/transactions
/lineups
/simulations
/backtests
/analytics
/dashboard
/admin
/models
/warehouse
/data-quality

Multi-Sport Expansion

/nfl
/nba
/nhl
/soccer
/esports
"""