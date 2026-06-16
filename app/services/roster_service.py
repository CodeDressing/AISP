# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 1.01 PART 2
# ENTERPRISE MLB ROSTER INGESTION SERVICE
# FILE: app/services/roster_service.py
# PURPOSE: sync MLB teams, rosters, players, and season stats into the master database
# ============================================================

import json

from sqlalchemy.orm import Session

from app.data_sources.mlb_stats_api import MLBStatsAPIClient
from app.database.models import Player, PlayerSeasonStat, RosterEntry, Team


# ============================================================
# SECTION 01 - ROSTER SERVICE
# ============================================================

class RosterService:
    def __init__(self, db: Session, client: MLBStatsAPIClient | None = None) -> None:
        self.db = db
        self.client = client or MLBStatsAPIClient()

    def sync_teams_and_rosters(self, season: int = 2026) -> dict:
        teams = self.client.get_teams(season=season)

        team_count = 0
        player_count = 0
        roster_count = 0
        stat_count = 0

        for item in teams:
            team = self._upsert_team(item)
            team_count += 1

            roster = self.client.get_roster(team.mlb_team_id, season=season)

            for roster_item in roster:
                person = roster_item.get("person", {})
                position = roster_item.get("position", {}).get("abbreviation")
                player_id = person.get("id")

                if not player_id:
                    continue

                detail = self.client.get_player(player_id) or person
                player = self._upsert_player(detail, team, position)

                self._upsert_roster_entry(
                    season=season,
                    team=team,
                    player=player,
                    roster_item=roster_item,
                    position=position,
                )

                player_count += 1
                roster_count += 1

                stat_count += self._sync_player_stats(
                    season=season,
                    player=player,
                    team=team,
                )

        self.db.commit()

        return {
            "season": season,
            "teams_synced": team_count,
            "players_synced": player_count,
            "roster_entries_synced": roster_count,
            "player_stat_rows_synced": stat_count,
        }


# ============================================================
# SECTION 02 - TEAM UPSERT LOGIC
# ============================================================

    def _upsert_team(self, item: dict) -> Team:
        team = self.db.query(Team).filter(Team.mlb_team_id == item["id"]).first()

        if team is None:
            team = Team(
                mlb_team_id=item["id"],
                name=item.get("name", "Unknown"),
            )
            self.db.add(team)

        team.name = item.get("name")
        team.abbreviation = item.get("abbreviation")
        team.league = item.get("league", {}).get("name")
        team.division = item.get("division", {}).get("name")
        team.venue_name = item.get("venue", {}).get("name")
        team.active = str(item.get("active"))

        return team


# ============================================================
# SECTION 03 - PLAYER UPSERT LOGIC
# ============================================================

    def _upsert_player(self, item: dict, team: Team, position: str | None) -> Player:
        player = self.db.query(Player).filter(Player.mlb_player_id == item["id"]).first()

        if player is None:
            player = Player(
                mlb_player_id=item["id"],
                full_name=item.get("fullName", "Unknown"),
            )
            self.db.add(player)

        player.full_name = item.get("fullName") or item.get("full_name") or "Unknown"
        player.current_team_id = team.mlb_team_id
        player.current_team_name = team.name
        player.position = position or item.get("primaryPosition", {}).get("abbreviation")
        player.bats = item.get("batSide", {}).get("code")
        player.throws = item.get("pitchHand", {}).get("code")
        player.height = item.get("height")
        player.weight = self._safe_int(item.get("weight"))
        player.birth_date = item.get("birthDate")
        player.birth_city = item.get("birthCity")
        player.birth_state = item.get("birthStateProvince")
        player.birth_country = item.get("birthCountry")
        player.mlb_debut_date = item.get("mlbDebutDate")
        player.active = str(item.get("active"))

        return player


# ============================================================
# SECTION 04 - ROSTER ENTRY UPSERT LOGIC
# ============================================================

    def _upsert_roster_entry(
        self,
        season: int,
        team: Team,
        player: Player,
        roster_item: dict,
        position: str | None,
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
        entry.roster_type = roster_item.get("rosterType")
        entry.jersey_number = roster_item.get("jerseyNumber")
        entry.position = position
        entry.status_code = roster_item.get("status", {}).get("code")
        entry.status_description = roster_item.get("status", {}).get("description")

        return entry


# ============================================================
# SECTION 05 - PLAYER STATS SYNC LOGIC
# ============================================================

    def _sync_player_stats(self, season: int, player: Player, team: Team) -> int:
        synced = 0

        for group_name in ["hitting", "pitching", "fielding"]:
            try:
                stats_payload = self.client.get_player_season_stats(
                    player_id=player.mlb_player_id,
                    season=season,
                    group=group_name,
                )
            except AttributeError:
                return 0
            except Exception:
                continue

            stat_blocks = stats_payload.get("stats", [])

            for stat_block in stat_blocks:
                stat_type = stat_block.get("type", {}).get("displayName", "season")

                for split in stat_block.get("splits", []):
                    stat = split.get("stat", {})

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
# SECTION 06 - PLAYER SEASON STAT UPSERT LOGIC
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
        row.games_played = self._safe_int(stat.get("gamesPlayed"))

        row.at_bats = self._safe_int(stat.get("atBats"))
        row.runs = self._safe_int(stat.get("runs"))
        row.hits = self._safe_int(stat.get("hits"))
        row.doubles = self._safe_int(stat.get("doubles"))
        row.triples = self._safe_int(stat.get("triples"))
        row.home_runs = self._safe_int(stat.get("homeRuns"))
        row.rbi = self._safe_int(stat.get("rbi"))
        row.stolen_bases = self._safe_int(stat.get("stolenBases"))
        row.strike_outs = self._safe_int(stat.get("strikeOuts"))
        row.base_on_balls = self._safe_int(stat.get("baseOnBalls"))
        row.batting_average = self._safe_float(stat.get("avg"))
        row.obp = self._safe_float(stat.get("obp"))
        row.slg = self._safe_float(stat.get("slg"))
        row.ops = self._safe_float(stat.get("ops"))

        row.wins = self._safe_int(stat.get("wins"))
        row.losses = self._safe_int(stat.get("losses"))
        row.era = self._safe_float(stat.get("era"))
        row.innings_pitched = stat.get("inningsPitched")
        row.whip = self._safe_float(stat.get("whip"))
        row.saves = self._safe_int(stat.get("saves"))

        row.raw_json = json.dumps(stat)

        return row


# ============================================================
# SECTION 07 - SAFE TYPE CONVERSION HELPERS
# ============================================================

    @staticmethod
    def _safe_int(value: object) -> int | None:
        try:
            if value in [None, "", "-", ".---"]:
                return None
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _safe_float(value: object) -> float | None:
        try:
            if value in [None, "", "-", ".---"]:
                return None
            return float(value)
        except (TypeError, ValueError):
            return None