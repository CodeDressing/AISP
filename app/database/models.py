# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 1.02 PART 1
# ENTERPRISE MASTER DATABASE EXPANSION
# FILE: app/database/models.py
# PURPOSE: scalable SQLAlchemy models for MLB rosters, players, games, stats, predictions, and AI chat history
# ============================================================

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from app.database.session import Base


# ============================================================
# SECTION 01 - TEAM MODEL
# ============================================================

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    mlb_team_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=True)
    league = Column(String, nullable=True)
    division = Column(String, nullable=True)
    venue_name = Column(String, nullable=True)
    active = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ============================================================
# SECTION 02 - PLAYER MODEL
# ============================================================

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    mlb_player_id = Column(Integer, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    current_team_id = Column(Integer, nullable=True)
    current_team_name = Column(String, nullable=True)
    position = Column(String, nullable=True)
    bats = Column(String, nullable=True)
    throws = Column(String, nullable=True)
    height = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    birth_date = Column(String, nullable=True)
    birth_city = Column(String, nullable=True)
    birth_state = Column(String, nullable=True)
    birth_country = Column(String, nullable=True)
    mlb_debut_date = Column(String, nullable=True)
    active = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ============================================================
# SECTION 03 - ROSTER HISTORY MODEL
# ============================================================

class RosterEntry(Base):
    __tablename__ = "roster_entries"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True, nullable=False)
    mlb_team_id = Column(Integer, index=True, nullable=False)
    mlb_player_id = Column(Integer, index=True, nullable=False)
    team_name = Column(String, nullable=True)
    player_name = Column(String, nullable=True)
    roster_type = Column(String, nullable=True)
    jersey_number = Column(String, nullable=True)
    position = Column(String, nullable=True)
    status_code = Column(String, nullable=True)
    status_description = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("season", "mlb_team_id", "mlb_player_id", name="uq_roster_season_team_player"),
    )


# ============================================================
# SECTION 04 - PLAYER SEASON STATS MODEL
# ============================================================

class PlayerSeasonStat(Base):
    __tablename__ = "player_season_stats"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True, nullable=False)
    mlb_player_id = Column(Integer, index=True, nullable=False)
    player_name = Column(String, nullable=True)
    mlb_team_id = Column(Integer, nullable=True)
    team_name = Column(String, nullable=True)
    group_name = Column(String, index=True, nullable=False)
    stat_type = Column(String, index=True, nullable=False)

    games_played = Column(Integer, nullable=True)

    at_bats = Column(Integer, nullable=True)
    runs = Column(Integer, nullable=True)
    hits = Column(Integer, nullable=True)
    doubles = Column(Integer, nullable=True)
    triples = Column(Integer, nullable=True)
    home_runs = Column(Integer, nullable=True)
    rbi = Column(Integer, nullable=True)
    stolen_bases = Column(Integer, nullable=True)
    strike_outs = Column(Integer, nullable=True)
    base_on_balls = Column(Integer, nullable=True)
    batting_average = Column(Float, nullable=True)
    obp = Column(Float, nullable=True)
    slg = Column(Float, nullable=True)
    ops = Column(Float, nullable=True)

    wins = Column(Integer, nullable=True)
    losses = Column(Integer, nullable=True)
    era = Column(Float, nullable=True)
    innings_pitched = Column(String, nullable=True)
    whip = Column(Float, nullable=True)
    saves = Column(Integer, nullable=True)

    raw_json = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("season", "mlb_player_id", "group_name", "stat_type", name="uq_player_stat_season_group"),
    )


# ============================================================
# SECTION 05 - GAME MODEL
# ============================================================

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    mlb_game_pk = Column(Integer, unique=True, index=True, nullable=False)
    season = Column(Integer, index=True, nullable=False)
    game_date = Column(String, index=True, nullable=True)
    official_date = Column(String, index=True, nullable=True)
    game_type = Column(String, nullable=True)
    status = Column(String, nullable=True)
    detailed_status = Column(String, nullable=True)
    venue_name = Column(String, nullable=True)

    home_team_id = Column(Integer, index=True, nullable=True)
    home_team_name = Column(String, nullable=True)
    away_team_id = Column(Integer, index=True, nullable=True)
    away_team_name = Column(String, nullable=True)

    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    winning_team_id = Column(Integer, nullable=True)
    losing_team_id = Column(Integer, nullable=True)

    raw_json = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ============================================================
# SECTION 06 - GAME TEAM MODEL
# ============================================================

class GameTeam(Base):
    __tablename__ = "game_teams"

    id = Column(Integer, primary_key=True, index=True)
    mlb_game_pk = Column(Integer, index=True, nullable=False)
    season = Column(Integer, index=True, nullable=False)
    mlb_team_id = Column(Integer, index=True, nullable=False)
    team_name = Column(String, nullable=True)
    side = Column(String, index=True, nullable=False)

    score = Column(Integer, nullable=True)
    hits = Column(Integer, nullable=True)
    errors = Column(Integer, nullable=True)
    is_winner = Column(String, nullable=True)

    raw_json = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("mlb_game_pk", "mlb_team_id", name="uq_game_team"),
    )


# ============================================================
# SECTION 07 - GAME PLAYER MODEL
# ============================================================

class GamePlayer(Base):
    __tablename__ = "game_players"

    id = Column(Integer, primary_key=True, index=True)
    mlb_game_pk = Column(Integer, index=True, nullable=False)
    season = Column(Integer, index=True, nullable=False)
    mlb_team_id = Column(Integer, index=True, nullable=True)
    team_name = Column(String, nullable=True)
    mlb_player_id = Column(Integer, index=True, nullable=False)
    player_name = Column(String, nullable=True)
    position = Column(String, nullable=True)

    batting_order = Column(String, nullable=True)
    is_starting = Column(String, nullable=True)

    at_bats = Column(Integer, nullable=True)
    runs = Column(Integer, nullable=True)
    hits = Column(Integer, nullable=True)
    home_runs = Column(Integer, nullable=True)
    rbi = Column(Integer, nullable=True)
    base_on_balls = Column(Integer, nullable=True)
    strike_outs = Column(Integer, nullable=True)

    innings_pitched = Column(String, nullable=True)
    earned_runs = Column(Integer, nullable=True)
    pitches_thrown = Column(Integer, nullable=True)

    raw_json = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("mlb_game_pk", "mlb_player_id", name="uq_game_player"),
    )


# ============================================================
# SECTION 08 - INJURY MODEL
# ============================================================

class Injury(Base):
    __tablename__ = "injuries"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True, nullable=True)
    mlb_player_id = Column(Integer, index=True, nullable=True)
    player_name = Column(String, nullable=True)
    mlb_team_id = Column(Integer, index=True, nullable=True)
    team_name = Column(String, nullable=True)

    injury_date = Column(String, index=True, nullable=True)
    injury_status = Column(String, nullable=True)
    injury_description = Column(Text, nullable=True)
    expected_return = Column(String, nullable=True)
    source = Column(String, nullable=True)

    raw_json = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ============================================================
# SECTION 09 - TRANSACTION MODEL
# ============================================================

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    mlb_transaction_id = Column(String, unique=True, index=True, nullable=True)
    season = Column(Integer, index=True, nullable=True)
    transaction_date = Column(String, index=True, nullable=True)
    effective_date = Column(String, nullable=True)

    mlb_player_id = Column(Integer, index=True, nullable=True)
    player_name = Column(String, nullable=True)
    from_team_id = Column(Integer, nullable=True)
    from_team_name = Column(String, nullable=True)
    to_team_id = Column(Integer, nullable=True)
    to_team_name = Column(String, nullable=True)

    transaction_type = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    raw_json = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ============================================================
# SECTION 10 - TEAM SEASON STATS MODEL
# ============================================================

class TeamSeasonStat(Base):
    __tablename__ = "team_season_stats"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True, nullable=False)
    mlb_team_id = Column(Integer, index=True, nullable=False)
    team_name = Column(String, nullable=True)
    group_name = Column(String, index=True, nullable=False)
    stat_type = Column(String, index=True, nullable=False)

    games_played = Column(Integer, nullable=True)
    wins = Column(Integer, nullable=True)
    losses = Column(Integer, nullable=True)
    runs = Column(Integer, nullable=True)
    hits = Column(Integer, nullable=True)
    home_runs = Column(Integer, nullable=True)
    rbi = Column(Integer, nullable=True)
    batting_average = Column(Float, nullable=True)
    obp = Column(Float, nullable=True)
    slg = Column(Float, nullable=True)
    ops = Column(Float, nullable=True)

    era = Column(Float, nullable=True)
    whip = Column(Float, nullable=True)
    strike_outs = Column(Integer, nullable=True)
    base_on_balls = Column(Integer, nullable=True)

    raw_json = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("season", "mlb_team_id", "group_name", "stat_type", name="uq_team_stat_season_group"),
    )


# ============================================================
# SECTION 11 - PLAYER ADVANCED METRICS MODEL
# ============================================================

class PlayerAdvancedMetric(Base):
    __tablename__ = "player_advanced_metrics"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True, nullable=False)
    mlb_player_id = Column(Integer, index=True, nullable=False)
    player_name = Column(String, nullable=True)
    mlb_team_id = Column(Integer, index=True, nullable=True)
    team_name = Column(String, nullable=True)

    war = Column(Float, nullable=True)
    woba = Column(Float, nullable=True)
    wrc_plus = Column(Float, nullable=True)
    ops_plus = Column(Float, nullable=True)
    babip = Column(Float, nullable=True)
    iso = Column(Float, nullable=True)
    xba = Column(Float, nullable=True)
    xslg = Column(Float, nullable=True)
    xwoba = Column(Float, nullable=True)

    fip = Column(Float, nullable=True)
    xfip = Column(Float, nullable=True)
    siera = Column(Float, nullable=True)
    k_rate = Column(Float, nullable=True)
    bb_rate = Column(Float, nullable=True)
    hr_per_9 = Column(Float, nullable=True)

    raw_json = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("season", "mlb_player_id", name="uq_player_advanced_metric_season"),
    )


# ============================================================
# SECTION 12 - STATCAST EVENT MODEL
# ============================================================

class StatcastEvent(Base):
    __tablename__ = "statcast_events"

    id = Column(Integer, primary_key=True, index=True)
    mlb_game_pk = Column(Integer, index=True, nullable=True)
    season = Column(Integer, index=True, nullable=True)
    game_date = Column(String, index=True, nullable=True)

    batter_id = Column(Integer, index=True, nullable=True)
    batter_name = Column(String, nullable=True)
    pitcher_id = Column(Integer, index=True, nullable=True)
    pitcher_name = Column(String, nullable=True)
    mlb_team_id = Column(Integer, index=True, nullable=True)
    team_name = Column(String, nullable=True)

    event_type = Column(String, index=True, nullable=True)
    description = Column(Text, nullable=True)
    pitch_type = Column(String, nullable=True)
    release_speed = Column(Float, nullable=True)
    launch_speed = Column(Float, nullable=True)
    launch_angle = Column(Float, nullable=True)
    hit_distance = Column(Float, nullable=True)
    estimated_ba = Column(Float, nullable=True)
    estimated_woba = Column(Float, nullable=True)

    raw_json = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# SECTION 13 - PREDICTION RUN MODEL
# ============================================================

class PredictionRun(Base):
    __tablename__ = "prediction_runs"

    id = Column(Integer, primary_key=True, index=True)
    prediction_type = Column(String, index=True, nullable=False)
    subject = Column(String, nullable=False)
    model_name = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    prediction_text = Column(Text, nullable=False)
    raw_features = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# SECTION 14 - GAME PREDICTION MODEL
# ============================================================

class GamePrediction(Base):
    __tablename__ = "game_predictions"

    id = Column(Integer, primary_key=True, index=True)
    mlb_game_pk = Column(Integer, index=True, nullable=True)
    season = Column(Integer, index=True, nullable=True)

    home_team_id = Column(Integer, index=True, nullable=True)
    home_team_name = Column(String, nullable=True)
    away_team_id = Column(Integer, index=True, nullable=True)
    away_team_name = Column(String, nullable=True)

    predicted_home_score = Column(Float, nullable=True)
    predicted_away_score = Column(Float, nullable=True)
    predicted_winner_team_id = Column(Integer, nullable=True)
    predicted_winner_team_name = Column(String, nullable=True)
    home_win_probability = Column(Float, nullable=True)
    away_win_probability = Column(Float, nullable=True)

    model_name = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    reasoning = Column(Text, nullable=True)
    raw_features = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# SECTION 15 - PLAYER PREDICTION MODEL
# ============================================================

class PlayerPrediction(Base):
    __tablename__ = "player_predictions"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True, nullable=True)
    mlb_game_pk = Column(Integer, index=True, nullable=True)
    mlb_player_id = Column(Integer, index=True, nullable=False)
    player_name = Column(String, nullable=True)
    mlb_team_id = Column(Integer, index=True, nullable=True)
    team_name = Column(String, nullable=True)

    prediction_market = Column(String, index=True, nullable=True)
    predicted_value = Column(Float, nullable=True)
    probability_over = Column(Float, nullable=True)
    probability_under = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)

    model_name = Column(String, nullable=True)
    reasoning = Column(Text, nullable=True)
    raw_features = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# SECTION 16 - MODEL BACKTEST MODEL
# ============================================================

class ModelBacktest(Base):
    __tablename__ = "model_backtests"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True, nullable=False)
    sport = Column(String, index=True, nullable=False)
    league = Column(String, index=True, nullable=False)
    market = Column(String, index=True, nullable=True)

    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    total_predictions = Column(Integer, nullable=True)
    correct_predictions = Column(Integer, nullable=True)
    accuracy = Column(Float, nullable=True)
    roi = Column(Float, nullable=True)
    profit_loss = Column(Float, nullable=True)

    notes = Column(Text, nullable=True)
    raw_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# SECTION 17 - AI CHAT SESSION MODEL
# ============================================================

class AIChatSession(Base):
    __tablename__ = "ai_chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, nullable=True)
    user_label = Column(String, nullable=True)
    sport = Column(String, index=True, nullable=True)
    league = Column(String, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================================
# SECTION 18 - AI CHAT MESSAGE MODEL
# ============================================================

class AIChatMessage(Base):
    __tablename__ = "ai_chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, index=True, nullable=False)
    role = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    model_name = Column(String, nullable=True)
    raw_context = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())