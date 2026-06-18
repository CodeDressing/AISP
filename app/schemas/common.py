# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 3.32 PART 1
# ENTERPRISE SHARED API SCHEMAS
# FILE: app/schemas/common.py
# PURPOSE: shared request/response models for chat,
# predictions, teams, players, health checks, analytics,
# and future sportsbook intelligence
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from pydantic import BaseModel
from pydantic import Field


# ============================================================
# SECTION 02 - CHAT SCHEMAS
# ============================================================

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        description="Natural language user message",
    )


class ChatResponse(BaseModel):
    intent: str
    status: str
    answer: str | None = None


# ============================================================
# SECTION 03 - GENERIC PREDICTION SCHEMAS
# ============================================================

class PredictionResponse(BaseModel):
    label: str
    probability: float
    explanation: str


# ============================================================
# SECTION 04 - PLAYER SEARCH SCHEMAS
# ============================================================

class PlayerSearchRequest(BaseModel):
    query: str


class PlayerSummary(BaseModel):
    player_id: int
    name: str
    team: str | None = None
    position: str | None = None


# ============================================================
# SECTION 05 - TEAM SCHEMAS
# ============================================================

class TeamSummary(BaseModel):
    team_id: int
    name: str
    abbreviation: str | None = None
    league: str | None = None
    division: str | None = None


# ============================================================
# SECTION 06 - HEALTH SCHEMAS
# ============================================================

class HealthResponse(BaseModel):
    status: str
    database: bool
    service: str


# ============================================================
# SECTION 07 - SYSTEM INFO SCHEMAS
# ============================================================

class SystemInfoResponse(BaseModel):
    app_name: str
    version: str
    environment: str
    debug: bool


# ============================================================
# SECTION 08 - GAME PREDICTION SCHEMAS
# ============================================================

class GamePredictionResponse(BaseModel):
    home_team: str
    away_team: str

    home_probability: float
    away_probability: float

    confidence: float


# ============================================================
# SECTION 09 - PLAYER PROP SCHEMAS
# ============================================================

class PlayerPropResponse(BaseModel):
    player_name: str
    market: str

    probability: float
    confidence: float

    explanation: str


# ============================================================
# SECTION 10 - DASHBOARD SCHEMAS
# ============================================================

class DashboardMetric(BaseModel):
    title: str
    value: str
    description: str | None = None


# ============================================================
# SECTION 11 - WAREHOUSE SCHEMAS
# ============================================================

class WarehouseStatusResponse(BaseModel):
    teams: int
    players: int
    games: int
    predictions: int


# ============================================================
# SECTION 12 - FUTURE ROADMAP
# ============================================================

"""
Future Schemas

StatcastResponse
InjuryResponse
TransactionResponse
SimulationResponse
BacktestResponse
SportsbookResponse
LeaderboardResponse
AnalyticsResponse
"""