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
from app.database.models import StatcastEvent



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
        mlb_team_id = self._safe_int(
            item.get("id")
        )

        if mlb_team_id is None:
            raise ValueError(
                "Cannot upsert team because MLB team id is missing."
            )

        team = (
            self.db.query(Team)
            .filter(
                Team.mlb_team_id == mlb_team_id,
            )
            .first()
        )

        if team is None:
            team = Team(
                mlb_team_id=mlb_team_id,
                name=(
                    item.get("name")
                    or "Unknown"
                ),
            )
            self.db.add(team)

        team.name = (
            item.get("name")
            or team.name
            or "Unknown"
        )
        team.abbreviation = item.get("abbreviation")
        team.league = item.get("league", {}).get("name")
        team.division = item.get("division", {}).get("name")
        team.venue_name = item.get("venue", {}).get("name")
        team.active = str(item.get("active"))

        return team


    def sync_teams_only(
        self,
        season: int = 2026,
    ) -> dict:
        self.errors = []

        teams = self.client.get_teams(
            season=season,
        )

        teams_found = len(teams)
        teams_synced = 0

        for team_item in teams:
            try:
                self._upsert_team(
                    team_item,
                )
                teams_synced += 1

            except Exception as exc:
                self._record_error(
                    scope="teams_only_sync",
                    identifier=team_item.get("id"),
                    error=exc,
                )

        self.db.commit()

        teams_in_database = (
            self.db.query(Team)
            .count()
        )

        return {
            "status": "success",
            "operation": "teams_only_sync",
            "season": season,
            "teams_found_from_mlb_api": teams_found,
            "teams_synced": teams_synced,
            "teams_in_database": teams_in_database,
            "errors": len(self.errors),
            "error_details": self.errors[:25],
        }
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
# SECTION 22 - STATCAST DATABASE INGESTION
# ============================================================

    def sync_statcast_range_to_database(
        self,
        start_date: str,
        end_date: str,
        season: int = 2026,
    ) -> dict:
        dataset = self.client.get_statcast_range(
            start_date=start_date,
            end_date=end_date,
        )

        deleted_rows = (
            self.db.query(StatcastEvent)
            .filter(
                StatcastEvent.game_date >= start_date,
                StatcastEvent.game_date <= end_date,
            )
            .delete(
                synchronize_session=False,
            )
        )

        inserted_rows = 0

        for _, row in dataset.iterrows():
            row_dict = {
                key: self._clean_statcast_value(value)
                for key, value in row.to_dict().items()
            }

            event = self._build_statcast_event(
                row_dict=row_dict,
                season=season,
            )

            self.db.add(event)
            inserted_rows += 1

        self.db.commit()

        return {
            "status": "success",
            "source": "baseball_savant_statcast",
            "start_date": start_date,
            "end_date": end_date,
            "season": season,
            "deleted_existing_rows": deleted_rows,
            "inserted_rows": inserted_rows,
            "columns": list(dataset.columns),
            "errors": self.errors[:25],
        }


# ============================================================
# SECTION 23 - STATCAST EVENT BUILDER
# ============================================================

    def _build_statcast_event(
        self,
        row_dict: dict[str, Any],
        season: int,
    ) -> StatcastEvent:
        event = StatcastEvent(
            mlb_game_pk=self._safe_int(
                row_dict.get("game_pk")
            ),
            season=season,
            game_date=row_dict.get("game_date"),

            batter_id=self._safe_int(
                row_dict.get("batter")
            ),
            batter_name=row_dict.get("player_name"),

            pitcher_id=self._safe_int(
                row_dict.get("pitcher")
            ),
            pitcher_name=None,

            mlb_team_id=None,
            team_name=row_dict.get("home_team"),

            event_type=row_dict.get("events"),
            description=row_dict.get("description"),
            pitch_type=row_dict.get("pitch_type"),

            release_speed=self._safe_float(
                row_dict.get("release_speed")
            ),
            launch_speed=self._safe_float(
                row_dict.get("launch_speed")
            ),
            launch_angle=self._safe_float(
                row_dict.get("launch_angle")
            ),
            hit_distance=self._safe_float(
                row_dict.get("hit_distance_sc")
            ),
            estimated_ba=self._safe_float(
                row_dict.get("estimated_ba_using_speedangle")
            ),
            estimated_woba=self._safe_float(
                row_dict.get("estimated_woba_using_speedangle")
            ),

            raw_json=json.dumps(
                row_dict,
                default=str,
            ),
            source="baseball_savant",
        )

        return event


# ============================================================
# SECTION 24 - STATCAST SAMPLE TEST
# ============================================================

    def run_statcast_sample(
        self,
        start_date: str,
        end_date: str,
    ) -> dict:
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
# SECTION 25 - PLAYER STATCAST PROFILE TEST
# ============================================================

    def sync_player_statcast_profile(
        self,
        player: Player,
        start_date: str,
        end_date: str,
    ) -> dict:
        result = {
            "player_id": player.mlb_player_id,
            "player_name": player.full_name,
            "batter_events": 0,
            "pitcher_events": 0,
        }

        try:
            batter_data = self.client.get_statcast_batter(
                player_id=player.mlb_player_id,
                start_date=start_date,
                end_date=end_date,
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
            pitcher_data = self.client.get_statcast_pitcher(
                player_id=player.mlb_player_id,
                start_date=start_date,
                end_date=end_date,
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

        result["errors"] = self.errors[:25]

        return result


# ============================================================
# SECTION 26 - ENTERPRISE DATA SOURCE STATUS
# ============================================================

    def build_data_source_status(
        self,
    ) -> dict:
        return {
            "mlb_stats_api": True,
            "baseball_savant": True,
            "statcast_database_ingestion": True,
            "fangraphs": False,
            "retrosheet": False,
            "lahman": False,
            "injury_feed": False,
            "weather_feed": False,
        }


# ============================================================
# SECTION 27 - STATCAST VALUE CLEANER
# ============================================================

    @staticmethod
    def _clean_statcast_value(
        value: object,
    ) -> object:
        if value is None:
            return None

        try:
            if value != value:
                return None
        except Exception:
            pass

        return value

# ============================================================
# SECTION 29 - FULL ROSTER INGESTION ENGINE
# ============================================================

    def sync_full_rosters(
        self,
        season: int = 2026,
    ) -> dict:
        """
        Pull every MLB team's full roster.

        This is a lighter sync than the complete
        enterprise warehouse sync and is intended
        to validate player ingestion before advanced
        stat and Statcast ingestion.
        """

        self.errors = []

        teams = (
            self.db.query(Team)
            .all()
        )

        teams_processed = 0
        players_processed = 0
        roster_entries_created = 0

        for team in teams:

            try:

                roster = self.client.get_roster(
                    team_id=team.mlb_team_id,
                    season=season,
                    roster_type="fullRoster",
                )

                teams_processed += 1

                for roster_item in roster:

                    try:

                        person = (
                            roster_item.get(
                                "person",
                                {},
                            )
                        )

                        position = (
                            roster_item
                            .get(
                                "position",
                                {},
                            )
                            .get(
                                "abbreviation"
                            )
                        )

                        player_id = (
                            person.get("id")
                        )

                        if not player_id:
                            continue

                        player_detail = (
                            self.client.get_player(
                                player_id
                            )
                            or person
                        )

                        player = (
                            self._upsert_player(
                                item=player_detail,
                                team=team,
                                position=position,
                            )
                        )

                        self._upsert_roster_entry(
                            season=season,
                            team=team,
                            player=player,
                            roster_item=roster_item,
                            position=position,
                            roster_type="fullRoster",
                        )

                        players_processed += 1
                        roster_entries_created += 1

                    except Exception as exc:

                        self._record_error(
                            scope="full_roster_player",
                            identifier=player_id,
                            error=exc,
                        )

                self.db.commit()

            except Exception as exc:

                self._record_error(
                    scope="full_roster_team",
                    identifier=team.mlb_team_id,
                    error=exc,
                )

                self.db.rollback()

        return {
            "status": "success",
            "operation": "full_roster_sync",
            "season": season,
            "teams_processed": teams_processed,
            "players_processed": players_processed,
            "roster_entries_created": roster_entries_created,
            "players_in_database": (
                self.db.query(Player)
                .count()
            ),
            "roster_entries_in_database": (
                self.db.query(RosterEntry)
                .count()
            ),
            "errors": len(
                self.errors
            ),
            "error_details": (
                self.errors[:25]
            ),
        }
# ============================================================
# SECTION 30 - WAREHOUSE AUDIT ENGINE
# ============================================================

    def build_warehouse_audit(
        self,
    ) -> dict:

        teams = (
            self.db.query(Team)
            .count()
        )

        players = (
            self.db.query(Player)
            .count()
        )

        roster_entries = (
            self.db.query(RosterEntry)
            .count()
        )

        player_stats = (
            self.db.query(
                PlayerSeasonStat
            ).count()
        )

        statcast_events = (
            self.db.query(
                StatcastEvent
            ).count()
        )

        completion_score = 0

        if teams > 0:
            completion_score += 20

        if players > 0:
            completion_score += 20

        if roster_entries > 0:
            completion_score += 20

        if player_stats > 0:
            completion_score += 20

        if statcast_events > 0:
            completion_score += 20

        return {
            "warehouse_score": completion_score,
            "teams": teams,
            "players": players,
            "roster_entries": roster_entries,
            "player_stats": player_stats,
            "statcast_events": statcast_events,
            "status": (
                "ready"
                if completion_score >= 80
                else "building"
            ),
        }
# ============================================================
# SECTION 28 - WAREHOUSE EXPANSION ROADMAP
# ============================================================

"""
Phase 4.15
Expose POST /admin/sync/statcast/range

Phase 4.16
Dashboard Statcast database sync button

Phase 4.17
Statcast row counts and data quality scoring

Phase 4.18
Feature engineering from Statcast events

Phase 4.19
Neural network training datasets

Phase 5.00
Enterprise baseball intelligence platform
"""

