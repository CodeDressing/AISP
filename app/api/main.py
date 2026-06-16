# SECTION 1: Imports
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.chatbot.router import AISPChatbotRouter
from app.core.config import settings
from app.database.models import Player, Team
from app.database.session import Base, engine, get_db
from app.schemas.common import ChatRequest


# SECTION 2: App Setup
Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="0.1.0")
chatbot = AISPChatbotRouter()


# SECTION 3: Health Routes
@app.get("/")
def root() -> dict:
    return {"app": settings.app_name, "status": "running", "python": "3.14-ready"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# SECTION 4: Team and Player Routes
@app.get("/teams")
def list_teams(db: Session = Depends(get_db)) -> list[dict]:
    teams = db.query(Team).order_by(Team.name).all()
    return [{"id": team.mlb_team_id, "name": team.name, "abbreviation": team.abbreviation} for team in teams]


@app.get("/players/search")
def search_players(q: str, db: Session = Depends(get_db)) -> list[dict]:
    players = db.query(Player).filter(Player.full_name.ilike(f"%{q}%")).limit(25).all()
    return [
        {
            "id": player.mlb_player_id,
            "name": player.full_name,
            "team": player.current_team_name,
            "position": player.position,
        }
        for player in players
    ]


# SECTION 5: Chatbot Route
@app.post("/chat")
def chat(request: ChatRequest) -> dict:
    return chatbot.answer(request.message)
