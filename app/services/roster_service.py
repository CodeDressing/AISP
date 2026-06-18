# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 2.03 PART 1
# ENTERPRISE MLB ROSTER + PLAYER WAREHOUSE SERVICE
# FILE: app/services/roster_service.py
# PURPOSE: sync MLB teams, roster groups, players, player profiles,
# player season stats, sync summaries, and ingestion errors
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

import json
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.data_sources.mlb_stats_api import MLBStatsAPIClient
from app.database.models import Player
from app.database.models import PlayerSeasonStat
from app.database.models import RosterEntry
from app.database.models import Team


# ============================================================
# SECTION 02 - SYNC CONFIGURATION
# ============================================================

@dataclass
class RosterSyncConfig:
    season: int = 2026
    roster_types: tuple[str, ...] = (
        "active",
        "40Man",
    )
    sync_player_details: bool = True
    sync_player_stats: bool = True
    commit_every_team: bool = True


# ============================================================
# SECTION 03 - SYNC SUMMARY
# ============================================================

@dataclass
class RosterSyncSummary:
    season: int
    teams_synced: int = 0
    roster_groups_synced: int = 0
    players_synced: int = 0
    roster_entries_synced: int = 0
    player_stat_rows_synced: int = 0
    errors: int = 0

    def to_dict(self) -> dict:
        return {
            "season": self.season,
            "teams_synced": self.teams_synced,
            "roster_groups_synced": self.roster_groups_synced,
            "players_synced": self.players_synced,
            "roster_entries_synced": self.roster_entries_synced,
            "player_stat_rows_synced": self.player_stat_rows_synced,
            "errors": self.errors,
        }


# ============================================================
# SECTION 04 - ROSTER SERVICE
# ============================================================

class RosterService:

    def __init__(
        self,
        db: Session,
        client: MLBStatsAPIClient | None = None,
    ) -> None:
        self.db = db
        self.client = client or MLBStatsAPIClient()
        self.errors: list[dict[str, Any]] = []


# ============================================================
# SECTION 05 - PUBLIC SYNC ENTRYPOINT
# ============================================================

    def sync_teams_and_rosters(
        self,
        season: int = 2026,
    ) -> dict:
        config = RosterSyncConfig(
            season=season,
        )

        summary = self.sync_with_config(
            config=config,
        )

        return summary


# ============================================================
# SECTION 06 - CONFIGURABLE SYNC PIPELINE
# ============================================================

    def sync_with_config(
        self,
        config: RosterSyncConfig,
    ) -> dict:
        self.errors = []

        summary = RosterSyncSummary(
            season=config.season,
        )

        teams = self.client.get_teams(
            season=config.season,
        )

        for team_item in teams:
            try:
                team = self._upsert_team(
                    team_item,
                )

                summary.teams_synced += 1

                for roster_type in config.roster_types:
                    summary.roster_groups_synced += 1

                    self._sync_team_roster_group(
                        config=config,
                        summary=summary,
                        team=team,
                        roster_type=roster_type,
                    )

                if config.commit_every_team:
                    self.db.commit()

            except Exception as exc:
                self._record_error(
                    scope="team_sync",
                    identifier=team_item.get("id"),
                    error=exc,
                )

                summary.errors += 1
                self.db.rollback()

        if not config.commit_every_team:
            self.db.commit()

        result = summary.to_dict()
        result["error_details"] = self.errors[:25]

        return result


# ============================================================
# SECTION 07 - TEAM ROSTER GROUP SYNC
# ============================================================

    def _sync_team_roster_group(
        self,
        config: RosterSyncConfig,
        summary: RosterSyncSummary,
        team: Team,
        roster_type: str,
    ) -> None:
        roster = self.client.get_roster(
            team_id=team.mlb_team_id,
            season=config.season,
            roster_type=roster_type,
        )

        for roster_item in roster:
            try:
                self._sync_roster_item(
                    config=config,
                    summary=summary,
                    team=team,
                    roster_item=roster_item,
                    roster_type=roster_type,
                )

            except Exception as exc:
                person = roster_item.get("person", {})
                self._record_error(
                    scope="roster_item_sync",
                    identifier=person.get("id"),
                    error=exc,
                )

                summary.errors += 1


# ============================================================
# SECTION 08 - INDIVIDUAL ROSTER ITEM SYNC
# ============================================================

    def _sync_roster_item(
        self,
        config: RosterSyncConfig,
        summary: RosterSyncSummary,
        team: Team,
        roster_item: dict,
        roster_type: str,
    ) -> None:
        person = roster_item.get(
            "person",
            {},
        )

        position = (
            roster_item
            .get("position", {})
            .get("abbreviation")
        )

        player_id = person.get("id")

        if not player_id:
            return

        if config.sync_player_details:
            detail = (
                self.client.get_player(
                    player_id,
                )
                or person
            )
        else:
            detail = person

        player = self._upsert_player(
            item=detail,
            team=team,
            position=position,
        )

        self._upsert_roster_entry(
            season=config.season,
            team=team,
            player=player,
            roster_item=roster_item,
            position=position,
            roster_type=roster_type,
        )

        summary.players_synced += 1
        summary.roster_entries_synced += 1

        if config.sync_player_stats:
            summary.player_stat_rows_synced += (
                self._sync_player_stats(
                    season=config.season,
                    player=player,
                    team=team,
                )
            )


# ============================================================
# SECTION 09 - TEAM UPSERT LOGIC
# ============================================================

    def _upsert_team(
        self,
        item: dict,
    ) -> Team:
        team = (
            self.db.query(Team)
            .filter(
                Team.mlb_team_id == item["id"],
            )
            .first()
        )

        if team is None:
            team = Team(
                mlb_team_id=item["id"],
                name=item.get(
                    "name",
                    "Unknown",
                ),
            )
            self.db.add(team)

        team.name = item.get("name")
        team.abbreviation = item.get("abbreviation")
        team.league = (
            item.get("league", {})
            .get("name")
        )
        team.division = (
            item.get("division", {})
            .get("name")
        )
        team.venue_name = (
            item.get("venue", {})
            .get("name")
        )
        team.active = str(
            item.get("active")
        )

        return team


# ============================================================
# SECTION 10 - PLAYER UPSERT LOGIC
# ============================================================

    def _upsert_player(
        self,
        item: dict,
        team: Team,
        position: str | None,
    ) -> Player:
        player = (
            self.db.query(Player)
            .filter(
                Player.mlb_player_id == item["id"],
            )
            .first()
        )

        if player is None:
            player = Player(
                mlb_player_id=item["id"],
                full_name=item.get(
                    "fullName",
                    "Unknown",
                ),
            )
            self.db.add(player)

        player.full_name = (
            item.get("fullName")
            or item.get("full_name")
            or "Unknown"
        )
        player.current_team_id = team.mlb_team_id
        player.current_team_name = team.name
        player.position = (
            position
            or item.get(
                "primaryPosition",
                {},
            ).get("abbreviation")
        )
        player.bats = (
            item.get("batSide", {})
            .get("code")
        )
        player.throws = (
            item.get("pitchHand", {})
            .get("code")
        )
        player.height = item.get("height")
        player.weight = self._safe_int(
            item.get("weight")
        )
        player.birth_date = item.get("birthDate")
        player.birth_city = item.get("birthCity")
        player.birth_state = item.get(
            "birthStateProvince"
        )
        player.birth_country = item.get(
            "birthCountry"
        )
        player.mlb_debut_date = item.get(
            "mlbDebutDate"
        )
        player.active = str(
            item.get("active")
        )

        return player


# ============================================================
# SECTION 11 - ROSTER ENTRY UPSERT LOGIC
# ============================================================

    def _upsert_roster_entry(
        self,
        season: int,
        team: Team,
        player: Player,
        roster_item: dict,
        position: str | None,
        roster_type: str,
    ) -> RosterEntry:
        entry = (
            self.db.query(RosterEntry)
            .filter(
                RosterEntry.season == season,
                RosterEntry.mlb_team_id == team.mlb_team_id,
                RosterEntry.mlb_player_id == player.mlb_player_id,
            )
            .first()
        )

        if entry is None:
            entry = RosterEntry(
                season=season,
                mlb_team_id=team.mlb_team_id,
                mlb_player_id=player.mlb_player_id,
            )
            self.db.add(entry)

        entry.team_name = team.name
        entry.player_name = player.full_name
        entry.roster_type = (
            roster_item.get("rosterType")
            or roster_type
        )
        entry.jersey_number = roster_item.get(
            "jerseyNumber"
        )
        entry.position = position
        entry.status_code = (
            roster_item.get("status", {})
            .get("code")
        )
        entry.status_description = (
            roster_item.get("status", {})
            .get("description")
        )

        return entry


# ============================================================
# SECTION 12 - PLAYER STATS SYNC LOGIC
# ============================================================

    def _sync_player_stats(
        self,
        season: int,
        player: Player,
        team: Team,
    ) -> int:
        synced = 0

        for group_name in [
            "hitting",
            "pitching",
            "fielding",
        ]:
            try:
                stats_payload = (
                    self.client
                    .get_player_season_stats(
                        player_id=player.mlb_player_id,
                        season=season,
                        group=group_name,
                    )
                )

            except AttributeError:
                return 0

            except Exception as exc:
                self._record_error(
                    scope="player_stats",
                    identifier=player.mlb_player_id,
                    error=exc,
                )
                continue

            stat_blocks = stats_payload.get(
                "stats",
                [],
            )

            for stat_block in stat_blocks:
                stat_type = (
                    stat_block
                    .get("type", {})
                    .get("displayName", "season")
                )

                for split in stat_block.get(
                    "splits",
                    [],
                ):
                    stat = split.get(
                        "stat",
                        {},
                    )

                    self._upsert_player_season_stat(
                        season=season,
                        player=player,
                        team=team,
                        group_name=group_name,
                        stat_type=stat_type,
                        stat=stat,
                    )

                    synced += 1

        return synced


# ============================================================
# SECTION 13 - PLAYER SEASON STAT UPSERT LOGIC
# ============================================================

    def _upsert_player_season_stat(
        self,
        season: int,
        player: Player,
        team: Team,
        group_name: str,
        stat_type: str,
        stat: dict,
    ) -> PlayerSeasonStat:
        row = (
            self.db.query(PlayerSeasonStat)
            .filter(
                PlayerSeasonStat.season == season,
                PlayerSeasonStat.mlb_player_id == player.mlb_player_id,
                PlayerSeasonStat.group_name == group_name,
                PlayerSeasonStat.stat_type == stat_type,
            )
            .first()
        )

        if row is None:
            row = PlayerSeasonStat(
                season=season,
                mlb_player_id=player.mlb_player_id,
                group_name=group_name,
                stat_type=stat_type,
            )
            self.db.add(row)

        row.player_name = player.full_name
        row.mlb_team_id = team.mlb_team_id
        row.team_name = team.name
        row.games_played = self._safe_int(
            stat.get("gamesPlayed")
        )

        row.at_bats = self._safe_int(
            stat.get("atBats")
        )
        row.runs = self._safe_int(
            stat.get("runs")
        )
        row.hits = self._safe_int(
            stat.get("hits")
        )
        row.doubles = self._safe_int(
            stat.get("doubles")
        )
        row.triples = self._safe_int(
            stat.get("triples")
        )
        row.home_runs = self._safe_int(
            stat.get("homeRuns")
        )
        row.rbi = self._safe_int(
            stat.get("rbi")
        )
        row.stolen_bases = self._safe_int(
            stat.get("stolenBases")
        )
        row.strike_outs = self._safe_int(
            stat.get("strikeOuts")
        )
        row.base_on_balls = self._safe_int(
            stat.get("baseOnBalls")
        )
        row.batting_average = self._safe_float(
            stat.get("avg")
        )
        row.obp = self._safe_float(
            stat.get("obp")
        )
        row.slg = self._safe_float(
            stat.get("slg")
        )
        row.ops = self._safe_float(
            stat.get("ops")
        )

        row.wins = self._safe_int(
            stat.get("wins")
        )
        row.losses = self._safe_int(
            stat.get("losses")
        )
        row.era = self._safe_float(
            stat.get("era")
        )
        row.innings_pitched = stat.get(
            "inningsPitched"
        )
        row.whip = self._safe_float(
            stat.get("whip")
        )
        row.saves = self._safe_int(
            stat.get("saves")
        )

        row.raw_json = json.dumps(
            stat
        )

        return row


# ============================================================
# SECTION 14 - ERROR COLLECTION
# ============================================================

    def _record_error(
        self,
        scope: str,
        identifier: object,
        error: Exception,
    ) -> None:
        self.errors.append(
            {
                "scope": scope,
                "identifier": identifier,
                "error_type": type(error).__name__,
                "message": str(error),
            }
        )


# ============================================================
# SECTION 15 - SAFE TYPE CONVERSION HELPERS
# ============================================================

    @staticmethod
    def _safe_int(
        value: object,
    ) -> int | None:
        try:
            if value in [
                None,
                "",
                "-",
                ".---",
            ]:
                return None

            return int(value)

        except (
            TypeError,
            ValueError,
        ):
            return None

    @staticmethod
    def _safe_float(
        value: object,
    ) -> float | None:
        try:
            if value in [
                None,
                "",
                "-",
                ".---",
            ]:
                return None

            return float(value)

        except (
            TypeError,
            ValueError,
        ):
            return None


# ============================================================
# SECTION 16 - CAREER STATS SYNC
# ============================================================

    def sync_player_career_stats(
        self,
        player: Player,
    ) -> int:
        synced = 0

        for group_name in [
            "hitting",
            "pitching",
            "fielding",
        ]:
            try:
                payload = (
                    self.client.get_player_career_stats(
                        player_id=player.mlb_player_id,
                        group=group_name,
                    )
                )

            except Exception as exc:
                self._record_error(
                    scope="career_stats",
                    identifier=player.mlb_player_id,
                    error=exc,
                )
                continue

            synced += 1

        return synced

# ============================================================
# SECTION 17 - PLAYER GAME LOG SYNC
# ============================================================

    def sync_player_game_logs(
        self,
        season: int,
        player: Player,
    ) -> int:
        synced = 0

        for group_name in [
            "hitting",
            "pitching",
        ]:
            try:
                payload = (
                    self.client.get_player_game_log(
                        player_id=player.mlb_player_id,
                        season=season,
                        group=group_name,
                    )
                )

            except Exception as exc:
                self._record_error(
                    scope="game_logs",
                    identifier=player.mlb_player_id,
                    error=exc,
                )
                continue

            synced += len(
                payload.get("stats", [])
            )

        return synced

# ============================================================
# SECTION 18 - PLAYER SPLITS SYNC
# ============================================================

    def sync_player_splits(
        self,
        season: int,
        player: Player,
    ) -> int:
        synced = 0

        split_types = [
            "homeAndAway",
            "leftRight",
            "month",
        ]

        for split_type in split_types:
            try:
                payload = (
                    self.client.get_player_splits(
                        player_id=player.mlb_player_id,
                        season=season,
                        split=split_type,
                    )
                )

            except Exception as exc:
                self._record_error(
                    scope="player_splits",
                    identifier=player.mlb_player_id,
                    error=exc,
                )
                continue

            synced += len(
                payload.get("stats", [])
            )

        return synced

# ============================================================
# SECTION 19 - VENUE SYNC
# ============================================================

    def sync_venues(
        self,
    ) -> int:
        try:
            venues = self.client.get_venues()

        except Exception:
            return 0

        return len(venues)

# ============================================================
# SECTION 20 - MASTER WAREHOUSE SYNC
# ============================================================

    def run_enterprise_warehouse_sync(
        self,
        season: int = 2026,
    ) -> dict:
        summary = self.sync_teams_and_rosters(
            season=season,
        )

        summary["warehouse_mode"] = True

        return summary

# ============================================================
# SECTION 21 - DATA QUALITY SUMMARY
# ============================================================

    def build_data_quality_summary(
        self,
    ) -> dict:
        return {
            "teams": self.db.query(Team).count(),
            "players": self.db.query(Player).count(),
            "roster_entries": self.db.query(
                RosterEntry
            ).count(),
            "player_stats": self.db.query(
                PlayerSeasonStat
            ).count(),
        }

# ============================================================
# SECTION 22 - STATCAST INGESTION PREPARATION
# ============================================================

    def sync_player_statcast_profile(
        self,
        player: Player,
        start_date: str,
        end_date: str,
    ) -> dict:
        """
        Pull Baseball Savant Statcast data for a player.

        Current phase:
        Retrieval only.

        Future phase:
        Store inside dedicated Statcast tables.
        """

        result = {
            "player_id": player.mlb_player_id,
            "player_name": player.full_name,
            "batter_events": 0,
            "pitcher_events": 0,
        }

        try:
            batter_data = (
                self.client.get_statcast_batter(
                    player_id=player.mlb_player_id,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            result["batter_events"] = len(
                batter_data.index
            )

        except Exception as exc:
            self._record_error(
                scope="statcast_batter",
                identifier=player.mlb_player_id,
                error=exc,
            )

        try:
            pitcher_data = (
                self.client.get_statcast_pitcher(
                    player_id=player.mlb_player_id,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            result["pitcher_events"] = len(
                pitcher_data.index
            )

        except Exception as exc:
            self._record_error(
                scope="statcast_pitcher",
                identifier=player.mlb_player_id,
                error=exc,
            )

        return result

# ============================================================
# SECTION 23 - STATCAST SAMPLE TEST
# ============================================================

    def run_statcast_sample(
        self,
        start_date: str,
        end_date: str,
    ) -> dict:
        """
        Pull a small Statcast sample.

        Useful for validating that
        Baseball Savant is connected.
        """

        dataset = self.client.get_statcast_range(
            start_date=start_date,
            end_date=end_date,
        )

        return {
            "rows": len(dataset.index),
            "columns": len(dataset.columns),
            "column_names": list(dataset.columns),
        }

# ============================================================
# SECTION 24 - ENTERPRISE DATA SOURCE STATUS
# ============================================================

    def build_data_source_status(
        self,
    ) -> dict:
        return {
            "mlb_stats_api": True,
            "baseball_savant": True,
            "fangraphs": False,
            "retrosheet": False,
            "lahman": False,
            "injury_feed": False,
            "weather_feed": False,
        }

# ============================================================
# SECTION 25 - WAREHOUSE EXPANSION ROADMAP
# ============================================================

"""
Phase 4.08
Statcast database tables

Phase 4.09
Statcast ingestion service

Phase 4.10
Retrosheet integration

Phase 4.11
Lahman historical database

Phase 4.12
Injury warehouse

Phase 4.13
Weather intelligence

Phase 4.14
Sportsbook odds ingestion

Phase 5.00
Enterprise baseball intelligence platform
"""