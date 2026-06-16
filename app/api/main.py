# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 1.04 PART 1
# ENTERPRISE API FOUNDATION
# FILE: app/api/main.py
# PURPOSE: central API gateway for analytics, players,
# teams, predictions, AI chat, monitoring, and health checks
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from fastapi import Depends
from fastapi import FastAPI
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
from app.database.session import (
    Base,
    database_health_check,
    engine,
    get_db,
)
from app.schemas.common import ChatRequest


# ============================================================
# SECTION 02 - APPLICATION INITIALIZATION
# ============================================================

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

chatbot = AISPChatbotRouter()


# ============================================================
# SECTION 03 - ROOT ROUTES
# ============================================================

@app.get("/")
def root() -> dict:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
        "platform": "AISP",
    }


# ============================================================
# SECTION 04 - HEALTH ROUTES
# ============================================================

@app.get("/health")
def health() -> dict:
    return {
        "status": "healthy",
        "database": database_health_check(),
    }


@app.get("/health/database")
def database_health() -> dict:
    return {
        "database": database_health_check(),
    }


# ============================================================
# SECTION 05 - TEAM ROUTES
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
        }
        for team in teams
    ]


# ============================================================
# SECTION 06 - PLAYER ROUTES
# ============================================================

@app.get("/players/search")
def search_players(
    q: str,
    db: Session = Depends(get_db),
) -> list[dict]:

    players = (
        db.query(Player)
        .filter(Player.full_name.ilike(f"%{q}%"))
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
        return {"error": "player_not_found"}

    return {
        "player_id": player.mlb_player_id,
        "name": player.full_name,
        "team": player.current_team_name,
        "position": player.position,
        "bats": player.bats,
        "throws": player.throws,
        "birth_date": player.birth_date,
    }


# ============================================================
# SECTION 07 - GAME ROUTES
# ============================================================

@app.get("/games")
def get_games(
    db: Session = Depends(get_db),
) -> list[dict]:

    games = (
        db.query(Game)
        .limit(250)
        .all()
    )

    return [
        {
            "game_pk": game.mlb_game_pk,
            "home_team": game.home_team_name,
            "away_team": game.away_team_name,
            "status": game.status,
            "date": game.game_date,
        }
        for game in games
    ]


# ============================================================
# SECTION 08 - GAME PREDICTION ROUTES
# ============================================================

@app.get("/predictions/games")
def get_game_predictions(
    db: Session = Depends(get_db),
) -> list[dict]:

    rows = (
        db.query(GamePrediction)
        .order_by(GamePrediction.id.desc())
        .limit(100)
        .all()
    )

    return [
        {
            "game_pk": row.mlb_game_pk,
            "home_team": row.home_team_name,
            "away_team": row.away_team_name,
            "home_probability": row.home_win_probability,
            "away_probability": row.away_win_probability,
            "confidence": row.confidence,
        }
        for row in rows
    ]


# ============================================================
# SECTION 09 - PLAYER PREDICTION ROUTES
# ============================================================

@app.get("/predictions/players")
def get_player_predictions(
    db: Session = Depends(get_db),
) -> list[dict]:

    rows = (
        db.query(PlayerPrediction)
        .order_by(PlayerPrediction.id.desc())
        .limit(100)
        .all()
    )

    return [
        {
            "player_id": row.mlb_player_id,
            "player_name": row.player_name,
            "market": row.prediction_market,
            "prediction": row.predicted_value,
            "confidence": row.confidence,
        }
        for row in rows
    ]


# ============================================================
# SECTION 10 - AI CHAT ROUTES
# ============================================================

@app.post("/chat")
def chat(
    request: ChatRequest,
) -> dict:

    return chatbot.answer(
        request.message
    )


# ============================================================
# SECTION 11 - SYSTEM INFORMATION ROUTES
# ============================================================

@app.get("/system/info")
def system_info() -> dict:
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "prediction_engine": settings.prediction_engine_enabled,
        "ai_chat": settings.ai_chat_enabled,
    }


# ============================================================
# SECTION 12 - FUTURE API ROADMAP
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

NFL
NBA
NHL
Soccer
"""