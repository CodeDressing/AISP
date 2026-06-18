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

from fastapi.responses import HTMLResponse


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
<!DOCTYPE html>
<html>

<head>

<title>AISP Command Center</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{

    background:
    radial-gradient(circle at top left,#2563eb33,transparent 35%),
    radial-gradient(circle at top right,#06b6d433,transparent 25%),
    linear-gradient(180deg,#020617,#0f172a);

    color:white;
    font-family:Inter,Arial,sans-serif;
}

.hero{

    padding:100px 60px;
    text-align:center;
}

.logo{

    font-size:18px;
    color:#38bdf8;
    letter-spacing:3px;
    font-weight:800;
}

.title{

    font-size:72px;
    font-weight:900;
    margin-top:20px;
}

.subtitle{

    margin-top:20px;
    color:#cbd5e1;
    max-width:900px;
    margin-left:auto;
    margin-right:auto;
    line-height:1.7;
    font-size:20px;
}

.button-row{

    margin-top:40px;
}

.btn{

    display:inline-block;
    margin:8px;
    padding:14px 28px;
    border-radius:14px;
    text-decoration:none;
    font-weight:700;
}

.primary{

    background:#2563eb;
    color:white;
}

.secondary{

    border:1px solid #334155;
    color:white;
}

.metrics{

    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:20px;
    padding:0 60px;
}

.metric{

    background:#111827;
    border:1px solid #1f2937;
    border-radius:18px;
    padding:25px;
    text-align:center;
}

.metric-value{

    font-size:36px;
    font-weight:900;
}

.metric-label{

    color:#94a3b8;
    margin-top:8px;
}

.modules{

    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:24px;
    padding:60px;
}

.card{

    background:#111827;
    border:1px solid #1f2937;
    border-radius:22px;
    padding:30px;
}

.card h2{

    margin-bottom:14px;
}

.card p{

    color:#cbd5e1;
    line-height:1.6;
}

.roadmap{

    padding:60px;
}

.roadmap-box{

    background:#111827;
    border-radius:22px;
    border:1px solid #1f2937;
    padding:30px;
}

.footer{

    text-align:center;
    padding:40px;
    color:#64748b;
}

@media(max-width:1000px){

.metrics{
grid-template-columns:1fr 1fr;
}

.modules{
grid-template-columns:1fr;
}

.title{
font-size:48px;
}

}

</style>

</head>

<body>

<div class="hero">

<div class="logo">
AISP BASEBALL ANALYTICS
</div>

<div class="title">
Enterprise AI Sports Intelligence
</div>

<div class="subtitle">

Artificial Intelligence Sports Predictor.

A next-generation MLB analytics platform combining
player intelligence, team intelligence, predictive modeling,
AI-assisted analysis, database warehousing, and future
sportsbook intelligence.

</div>

<div class="button-row">

<a href="/docs" class="btn primary">
Open API Docs
</a>

<a href="/health" class="btn secondary">
System Health
</a>

<a href="/system/routes" class="btn secondary">
API Routes
</a>

</div>

</div>

<div class="metrics">

<div class="metric">
<div class="metric-value">MLB</div>
<div class="metric-label">Sport Module</div>
</div>

<div class="metric">
<div class="metric-value">AI</div>
<div class="metric-label">Prediction Layer</div>
</div>

<div class="metric">
<div class="metric-value">24/7</div>
<div class="metric-label">Analytics Engine</div>
</div>

<div class="metric">
<div class="metric-value">LIVE</div>
<div class="metric-label">Render Deployment</div>
</div>

</div>

<div class="modules">

<div class="card">

<h2>Player Intelligence</h2>

<p>
Player profiles, historical performance,
career trends, projections, and AI-assisted
analysis.
</p>

</div>

<div class="card">

<h2>Prediction Engine</h2>

<p>
Hit probabilities, home run models,
game predictions, simulations, and future
machine learning pipelines.
</p>

</div>

<div class="card">

<h2>AI Analyst</h2>

<p>
Natural language baseball research
powered by the AISP AI routing layer.
</p>

</div>

</div>

<div class="roadmap">

<div class="roadmap-box">

<h2>Platform Roadmap</h2>

<br>

<p>

Phase 4.01:
Enterprise Dashboard UI

<br><br>

Phase 4.02:
Player Cards, Team Cards, Leaderboards

<br><br>

Phase 4.03:
Statcast Visualizations

<br><br>

Phase 4.04:
Monte Carlo Simulation Engine

<br><br>

Phase 5.00:
Sportsbook Intelligence Platform

</p>

</div>

</div>

<div class="footer">

AISP Baseball Analytics Engine • Enterprise AI Sports Intelligence

</div>

</body>
</html>
"""
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
# SECTION 15 - SYSTEM INFORMATION, ROUTES & DATA SOURCE ROUTES
# ============================================================

from app.services.roster_service import RosterService


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
        "platform": "AISP Baseball Analytics Engine",
        "phase": "4.11",
    }


@app.get("/system/routes")
def system_routes() -> dict:
    return {
        "public_routes": [
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
        ],
        "admin_routes": [
            "/admin/sync/mlb",
            "/admin/database/summary",
            "/admin/system/status",
            "/admin/warehouse/metrics",
            "/admin/platform/readiness",
            "/admin/statcast/sample",
            "/admin/statcast/player/{player_id}",
            "/admin/data-sources/status",
        ],
        "data_sources": [
            "MLB Stats API",
            "Baseball Savant / Statcast",
        ],
    }


@app.get("/admin/data-sources/status")
def admin_data_sources_status(
    db: Session = Depends(get_db),
) -> dict:
    service = RosterService(
        db=db,
    )

    return service.build_data_source_status()


@app.get("/admin/statcast/sample")
def admin_statcast_sample(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
) -> dict:
    service = RosterService(
        db=db,
    )

    result = service.run_statcast_sample(
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "status": "success",
        "source": "baseball_savant_statcast",
        "start_date": start_date,
        "end_date": end_date,
        "result": result,
    }


@app.get("/admin/statcast/player/{player_id}")
def admin_player_statcast_profile(
    player_id: int,
    start_date: str,
    end_date: str,
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

    service = RosterService(
        db=db,
    )

    result = service.sync_player_statcast_profile(
        player=player,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "status": "success",
        "source": "baseball_savant_statcast",
        "player_id": player_id,
        "player_name": player.full_name,
        "start_date": start_date,
        "end_date": end_date,
        "result": result,
    }
# ============================================================
# SECTION 16 - ENTERPRISE ADMIN & WAREHOUSE ROUTES
# ============================================================

from app.services.roster_service import RosterService


@app.post("/admin/sync/mlb")
def admin_sync_mlb_database(
    season: int = 2026,
    db: Session = Depends(get_db),
) -> dict:
    """
    Enterprise warehouse synchronization.
    Pulls teams, rosters, players, and statistics
    from configured MLB data providers.
    """

    service = RosterService(
        db=db,
    )

    result = service.run_enterprise_warehouse_sync(
        season=season,
    )

    return {
        "status": "success",
        "operation": "enterprise_sync",
        "season": season,
        "result": result,
    }


@app.get("/admin/database/summary")
def admin_database_summary(
    db: Session = Depends(get_db),
) -> dict:
    """
    High-level warehouse summary.
    """

    return {
        "teams": db.query(Team).count(),
        "players": db.query(Player).count(),
        "games": db.query(Game).count(),
        "game_predictions": db.query(GamePrediction).count(),
        "player_predictions": db.query(PlayerPrediction).count(),
        "database_connected": check_database_connection(),
    }


@app.get("/admin/system/status")
def admin_system_status(
    db: Session = Depends(get_db),
) -> dict:
    """
    Enterprise platform status endpoint.
    """

    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "database_connected": check_database_connection(),
        "prediction_engine": settings.prediction_engine_enabled,
        "ai_chat": settings.ai_chat_enabled,
        "teams_loaded": db.query(Team).count(),
        "players_loaded": db.query(Player).count(),
        "games_loaded": db.query(Game).count(),
    }


@app.get("/admin/warehouse/metrics")
def warehouse_metrics(
    db: Session = Depends(get_db),
) -> dict:
    """
    Core warehouse metrics.
    """

    return {
        "total_teams": db.query(Team).count(),
        "total_players": db.query(Player).count(),
        "total_games": db.query(Game).count(),
        "total_game_predictions": db.query(GamePrediction).count(),
        "total_player_predictions": db.query(PlayerPrediction).count(),
    }


@app.get("/admin/platform/readiness")
def platform_readiness(
    db: Session = Depends(get_db),
) -> dict:
    """
    Enterprise readiness scoring.
    """

    score = 0

    if check_database_connection():
        score += 25

    if db.query(Team).count() > 0:
        score += 25

    if db.query(Player).count() > 0:
        score += 25

    if settings.ai_chat_enabled:
        score += 25

    return {
        "readiness_score": score,
        "max_score": 100,
        "status": (
            "enterprise_ready"
            if score >= 75
            else "in_progress"
        ),
    }

# ============================================================
# SECTION 16A - STATCAST / BASEBALL SAVANT TEST ROUTES
# ============================================================

@app.get("/admin/statcast/sample")
def admin_statcast_sample(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Pull a live Baseball Savant / Statcast sample.

    Example:
    /admin/statcast/sample?start_date=2025-04-01&end_date=2025-04-02
    """

    service = RosterService(
        db=db,
    )

    result = service.run_statcast_sample(
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "status": "success",
        "source": "baseball_savant_statcast",
        "start_date": start_date,
        "end_date": end_date,
        "result": result,
    }


@app.get("/admin/statcast/player/{player_id}")
def admin_player_statcast_profile(
    player_id: int,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Pull Baseball Savant / Statcast batter and pitcher event counts
    for one player.
    """

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

    service = RosterService(
        db=db,
    )

    result = service.sync_player_statcast_profile(
        player=player,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "status": "success",
        "source": "baseball_savant_statcast",
        "player_id": player_id,
        "start_date": start_date,
        "end_date": end_date,
        "result": result,
    }


@app.get("/admin/data-sources/status")
def admin_data_sources_status(
    db: Session = Depends(get_db),
) -> dict:
    """
    Show which data sources are currently connected or planned.
    """

    service = RosterService(
        db=db,
    )

    return service.build_data_source_status()

# ============================================================
# SECTION 17 - FUTURE API ROADMAP
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
/admin/sync/mlb
/admin/database/summary
/admin/system/status
/admin/warehouse/metrics
/admin/platform/readiness

Multi-Sport Expansion

/nfl
/nba
/nhl
/soccer
/esports
"""