# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 3.01 PART 1
# ENTERPRISE DATABASE-AWARE AI CHAT ROUTER
# FILE: app/chatbot/router.py
# PURPOSE: route natural language MLB questions into player lookup,
# team lookup, statistics lookup, prediction logic, and future AI tools
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from sqlalchemy.orm import Session

from app.database.models import Player
from app.database.models import PlayerSeasonStat
from app.database.models import Team
from app.database.session import SessionLocal
from app.prediction.baseline_model import BaselinePredictionEngine


# ============================================================
# SECTION 02 - CHATBOT ROUTER
# ============================================================

class AISPChatbotRouter:

    def __init__(self) -> None:
        self.prediction_engine = BaselinePredictionEngine()


# ============================================================
# SECTION 03 - MAIN MESSAGE ENTRYPOINT
# ============================================================

    def answer(self, message: str) -> dict:
        lowered = message.lower().strip()
        intent = self._detect_intent(lowered)

        db = SessionLocal()

        try:
            if intent == "prediction":
                return self._handle_prediction(message, db)

            if intent == "player_lookup":
                return self._handle_player_lookup(message, db)

            if intent == "team_lookup":
                return self._handle_team_lookup(message, db)

            if intent == "stats_lookup":
                return self._handle_stats_lookup(message, db)

            if intent == "simulation":
                return self._handle_simulation(message)

            return self._handle_general(message)

        finally:
            db.close()


# ============================================================
# SECTION 04 - INTENT DETECTION
# ============================================================

    def _detect_intent(self, message: str) -> str:
        prediction_keywords = [
            "predict",
            "prediction",
            "probability",
            "chance",
            "favorite",
            "winner",
            "win",
            "hit tonight",
            "home run",
        ]

        stats_keywords = [
            "stats",
            "average",
            "ops",
            "war",
            "era",
            "home runs",
            "hits",
            "rbi",
            "strikeouts",
        ]

        simulation_keywords = [
            "simulate",
            "simulation",
            "monte carlo",
        ]

        team_keywords = [
            "yankees",
            "mets",
            "dodgers",
            "red sox",
            "cubs",
            "braves",
            "phillies",
            "padres",
            "astros",
            "orioles",
        ]

        player_keywords = [
            "juan soto",
            "aaron judge",
            "shohei",
            "ohtani",
            "mookie",
            "betts",
            "mike trout",
            "bryce harper",
        ]

        if any(word in message for word in prediction_keywords):
            return "prediction"

        if any(word in message for word in stats_keywords):
            return "stats_lookup"

        if any(word in message for word in simulation_keywords):
            return "simulation"

        if any(word in message for word in player_keywords):
            return "player_lookup"

        if any(word in message for word in team_keywords):
            return "team_lookup"

        return "general"


# ============================================================
# SECTION 05 - PREDICTION HANDLER
# ============================================================

    def _handle_prediction(
        self,
        message: str,
        db: Session,
    ) -> dict:
        player = self._find_player_from_message(
            message=message,
            db=db,
        )

        if not player:
            result = self.prediction_engine.predict_player_hit_probability(
                0.275,
                0.820,
            )

            return {
                "intent": "prediction",
                "status": "baseline",
                "answer": f"Baseline prediction: {result.label}",
                "probability": result.probability,
                "explanation": result.explanation,
                "note": "No player was matched in the local database yet.",
            }

        stats = self._get_latest_player_stats(
            player_id=player.mlb_player_id,
            db=db,
        )

        batting_average = (
            stats.batting_average
            if stats and stats.batting_average is not None
            else 0.240
        )

        ops = (
            stats.ops
            if stats and stats.ops is not None
            else 0.700
        )

        result = self.prediction_engine.predict_player_hit_probability(
            batting_average,
            ops,
        )

        return {
            "intent": "prediction",
            "status": "success",
            "player": player.full_name,
            "team": player.current_team_name,
            "prediction": result.label,
            "probability": result.probability,
            "explanation": result.explanation,
            "input_features": {
                "batting_average": batting_average,
                "ops": ops,
            },
        }


# ============================================================
# SECTION 06 - PLAYER LOOKUP HANDLER
# ============================================================

    def _handle_player_lookup(
        self,
        message: str,
        db: Session,
    ) -> dict:
        player = self._find_player_from_message(
            message=message,
            db=db,
        )

        if not player:
            return {
                "intent": "player_lookup",
                "status": "not_found",
                "answer": "I could not find that player in the local MLB database yet. Run the master database builder first.",
            }

        stats = self._get_latest_player_stats(
            player_id=player.mlb_player_id,
            db=db,
        )

        response = {
            "intent": "player_lookup",
            "status": "success",
            "player": {
                "player_id": player.mlb_player_id,
                "name": player.full_name,
                "team": player.current_team_name,
                "position": player.position,
                "bats": player.bats,
                "throws": player.throws,
                "height": player.height,
                "weight": player.weight,
                "birth_date": player.birth_date,
                "active": player.active,
            },
        }

        if stats:
            response["latest_stats"] = self._format_player_stats(
                stats,
            )

        return response


# ============================================================
# SECTION 07 - TEAM LOOKUP HANDLER
# ============================================================

    def _handle_team_lookup(
        self,
        message: str,
        db: Session,
    ) -> dict:
        team = self._find_team_from_message(
            message=message,
            db=db,
        )

        if not team:
            return {
                "intent": "team_lookup",
                "status": "not_found",
                "answer": "I could not find that team in the local MLB database yet.",
            }

        players = (
            db.query(Player)
            .filter(Player.current_team_id == team.mlb_team_id)
            .order_by(Player.full_name)
            .limit(50)
            .all()
        )

        return {
            "intent": "team_lookup",
            "status": "success",
            "team": {
                "team_id": team.mlb_team_id,
                "name": team.name,
                "abbreviation": team.abbreviation,
                "league": team.league,
                "division": team.division,
                "venue": team.venue_name,
            },
            "roster_sample": [
                {
                    "player_id": player.mlb_player_id,
                    "name": player.full_name,
                    "position": player.position,
                }
                for player in players
            ],
        }


# ============================================================
# SECTION 08 - STATISTICS HANDLER
# ============================================================

    def _handle_stats_lookup(
        self,
        message: str,
        db: Session,
    ) -> dict:
        player = self._find_player_from_message(
            message=message,
            db=db,
        )

        if player:
            stats = self._get_latest_player_stats(
                player_id=player.mlb_player_id,
                db=db,
            )

            if not stats:
                return {
                    "intent": "stats_lookup",
                    "status": "missing_stats",
                    "player": player.full_name,
                    "answer": "Player found, but no season stats are stored yet.",
                }

            return {
                "intent": "stats_lookup",
                "status": "success",
                "player": player.full_name,
                "team": player.current_team_name,
                "stats": self._format_player_stats(stats),
            }

        leaders = (
            db.query(PlayerSeasonStat)
            .filter(PlayerSeasonStat.ops.isnot(None))
            .order_by(PlayerSeasonStat.ops.desc())
            .limit(10)
            .all()
        )

        return {
            "intent": "stats_lookup",
            "status": "leaderboard",
            "answer": "No specific player was matched, so I returned OPS leaders.",
            "ops_leaders": [
                {
                    "player": row.player_name,
                    "team": row.team_name,
                    "ops": row.ops,
                    "home_runs": row.home_runs,
                    "batting_average": row.batting_average,
                }
                for row in leaders
            ],
        }


# ============================================================
# SECTION 09 - SIMULATION HANDLER
# ============================================================

    def _handle_simulation(
        self,
        message: str,
    ) -> dict:
        return {
            "intent": "simulation",
            "status": "placeholder",
            "answer": "Monte Carlo simulation engine is planned for Phase 3.02.",
        }


# ============================================================
# SECTION 10 - GENERAL RESPONSE HANDLER
# ============================================================

    def _handle_general(
        self,
        message: str,
    ) -> dict:
        return {
            "intent": "general",
            "status": "success",
            "answer": "I can help with MLB players, teams, statistics, predictions, simulations, and analytics. Try asking: 'Show me Juan Soto stats' or 'Predict Aaron Judge hit probability.'",
        }


# ============================================================
# SECTION 11 - PLAYER NAME EXTRACTION
# ============================================================

    def _find_player_from_message(
        self,
        message: str,
        db: Session,
    ) -> Player | None:
        lowered = message.lower()

        known_names = [
            "juan soto",
            "aaron judge",
            "shohei ohtani",
            "ohtani",
            "mookie betts",
            "mike trout",
            "bryce harper",
        ]

        for name in known_names:
            if name in lowered:
                return (
                    db.query(Player)
                    .filter(Player.full_name.ilike(f"%{name}%"))
                    .first()
                )

        words = [
            word.strip(".,?!")
            for word in message.split()
            if len(word.strip(".,?!")) > 2
        ]

        if len(words) >= 2:
            possible_name = f"{words[-2]} {words[-1]}"

            player = (
                db.query(Player)
                .filter(Player.full_name.ilike(f"%{possible_name}%"))
                .first()
            )

            if player:
                return player

        return None


# ============================================================
# SECTION 12 - TEAM NAME EXTRACTION
# ============================================================

    def _find_team_from_message(
        self,
        message: str,
        db: Session,
    ) -> Team | None:
        lowered = message.lower()

        teams = (
            db.query(Team)
            .all()
        )

        for team in teams:
            if team.name and team.name.lower() in lowered:
                return team

            if team.abbreviation and team.abbreviation.lower() in lowered:
                return team

        aliases = {
            "yankees": "New York Yankees",
            "mets": "New York Mets",
            "dodgers": "Los Angeles Dodgers",
            "red sox": "Boston Red Sox",
            "cubs": "Chicago Cubs",
            "braves": "Atlanta Braves",
            "phillies": "Philadelphia Phillies",
            "padres": "San Diego Padres",
            "astros": "Houston Astros",
            "orioles": "Baltimore Orioles",
        }

        for alias, full_name in aliases.items():
            if alias in lowered:
                return (
                    db.query(Team)
                    .filter(Team.name.ilike(f"%{full_name}%"))
                    .first()
                )

        return None


# ============================================================
# SECTION 13 - PLAYER STAT LOOKUP
# ============================================================

    def _get_latest_player_stats(
        self,
        player_id: int,
        db: Session,
    ) -> PlayerSeasonStat | None:
        return (
            db.query(PlayerSeasonStat)
            .filter(PlayerSeasonStat.mlb_player_id == player_id)
            .filter(PlayerSeasonStat.group_name == "hitting")
            .order_by(PlayerSeasonStat.season.desc())
            .first()
        )


# ============================================================
# SECTION 14 - PLAYER STAT FORMATTER
# ============================================================

    def _format_player_stats(
        self,
        stats: PlayerSeasonStat,
    ) -> dict:
        return {
            "season": stats.season,
            "team": stats.team_name,
            "games_played": stats.games_played,
            "at_bats": stats.at_bats,
            "runs": stats.runs,
            "hits": stats.hits,
            "doubles": stats.doubles,
            "triples": stats.triples,
            "home_runs": stats.home_runs,
            "rbi": stats.rbi,
            "stolen_bases": stats.stolen_bases,
            "strikeouts": stats.strike_outs,
            "walks": stats.base_on_balls,
            "batting_average": stats.batting_average,
            "obp": stats.obp,
            "slg": stats.slg,
            "ops": stats.ops,
        }


# ============================================================
# SECTION 15 - FUTURE AI ROADMAP
# ============================================================

"""
Future Chat Router Upgrades

1. Natural language SQL
2. Database-aware game prediction
3. Player comparison engine
4. Team comparison engine
5. Statcast-aware answers
6. Injury-aware predictions
7. Transaction-aware roster context
8. Betting market interpretation
9. AI model explainability
10. RAG integration
11. Vector database integration
12. Multi-sport routing
"""