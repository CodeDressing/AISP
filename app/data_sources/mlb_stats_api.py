# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 1.01 PART 3
# ENTERPRISE MLB STATS API CLIENT
# FILE: app/data_sources/mlb_stats_api.py
# PURPOSE: reusable MLB Stats API client for teams, rosters, players, stats, schedules, and future prediction data
# ============================================================

from __future__ import annotations

from typing import Any

import requests

from app.core.config import settings


# ============================================================
# SECTION 01 - MLB STATS API CLIENT
# ============================================================

class MLBStatsAPIClient:
    def __init__(self, base_url: str | None = None, timeout: int = 30) -> None:
        self.base_url = base_url or settings.mlb_api_base_url
        self.timeout = timeout


# ============================================================
# SECTION 02 - CORE REQUEST HANDLER
# ============================================================

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

        response = requests.get(
            url,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()
        return response.json()


# ============================================================
# SECTION 03 - TEAM ENDPOINTS
# ============================================================

    def get_teams(self, season: int = 2026) -> list[dict[str, Any]]:
        payload = self._get(
            "teams",
            params={
                "sportId": 1,
                "season": season,
            },
        )

        return payload.get("teams", [])


# ============================================================
# SECTION 04 - ROSTER ENDPOINTS
# ============================================================

    def get_roster(
        self,
        team_id: int,
        season: int = 2026,
        roster_type: str = "active",
    ) -> list[dict[str, Any]]:
        payload = self._get(
            f"teams/{team_id}/roster",
            params={
                "season": season,
                "rosterType": roster_type,
            },
        )

        return payload.get("roster", [])


# ============================================================
# SECTION 05 - PLAYER PROFILE ENDPOINTS
# ============================================================

    def get_player(self, player_id: int) -> dict[str, Any]:
        payload = self._get(f"people/{player_id}")
        people = payload.get("people", [])

        if not people:
            return {}

        return people[0]


# ============================================================
# SECTION 06 - PLAYER SEASON STATS ENDPOINTS
# ============================================================

    def get_player_season_stats(
        self,
        player_id: int,
        season: int = 2026,
        group: str = "hitting",
    ) -> dict[str, Any]:
        return self._get(
            f"people/{player_id}/stats",
            params={
                "stats": "season",
                "season": season,
                "group": group,
            },
        )

    def get_player_stats(
        self,
        player_id: int,
        season: int = 2026,
        group: str = "hitting",
    ) -> dict[str, Any]:
        return self.get_player_season_stats(
            player_id=player_id,
            season=season,
            group=group,
        )


# ============================================================
# SECTION 07 - TEAM SEASON STATS ENDPOINTS
# ============================================================

    def get_team_season_stats(
        self,
        team_id: int,
        season: int = 2026,
        group: str = "hitting",
    ) -> dict[str, Any]:
        return self._get(
            f"teams/{team_id}/stats",
            params={
                "stats": "season",
                "season": season,
                "group": group,
            },
        )


# ============================================================
# SECTION 08 - SCHEDULE ENDPOINTS
# ============================================================

    def get_schedule(
        self,
        season: int = 2026,
        start_date: str | None = None,
        end_date: str | None = None,
        team_id: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "sportId": 1,
            "season": season,
        }

        if start_date:
            params["startDate"] = start_date

        if end_date:
            params["endDate"] = end_date

        if team_id:
            params["teamId"] = team_id

        return self._get("schedule", params=params)


# ============================================================
# SECTION 09 - GAME FEED ENDPOINTS
# ============================================================

    def get_game_feed(self, game_pk: int) -> dict[str, Any]:
        return self._get(f"game/{game_pk}/feed/live")


# ============================================================
# SECTION 10 - STANDINGS ENDPOINTS
# ============================================================

    def get_standings(self, season: int = 2026) -> dict[str, Any]:
        return self._get(
            "standings",
            params={
                "leagueId": "103,104",
                "season": season,
                "standingsTypes": "regularSeason",
            },
        )


# ============================================================
# SECTION 11 - TRANSACTION ENDPOINTS
# ============================================================

    def get_transactions(
        self,
        start_date: str,
        end_date: str,
        team_id: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "sportId": 1,
            "startDate": start_date,
            "endDate": end_date,
        }

        if team_id:
            params["teamId"] = team_id

        return self._get("transactions", params=params)


# ============================================================
# SECTION 12 - SEARCH / LOOKUP HELPERS
# ============================================================

    def search_player_by_name(self, name: str, season: int = 2026) -> list[dict[str, Any]]:
        payload = self._get(
            "sports/1/players",
            params={
                "season": season,
            },
        )

        players = payload.get("people", [])
        lowered_name = name.lower().strip()

        return [
            player
            for player in players
            if lowered_name in player.get("fullName", "").lower()
        ]

# ============================================================
# SECTION 13 - ALL ACTIVE MLB PLAYERS
# ============================================================

    def get_all_active_players(
        self,
        season: int = 2026,
    ) -> list[dict[str, Any]]:
        payload = self._get(
            "sports/1/players",
            params={
                "season": season,
            },
        )

        return payload.get(
            "people",
            [],
        )


# ============================================================
# SECTION 14 - PLAYER GAME LOG ENDPOINTS
# ============================================================

    def get_player_game_log(
        self,
        player_id: int,
        season: int = 2026,
        group: str = "hitting",
    ) -> dict[str, Any]:
        return self._get(
            f"people/{player_id}/stats",
            params={
                "stats": "gameLog",
                "season": season,
                "group": group,
            },
        )


# ============================================================
# SECTION 15 - PLAYER CAREER STATS ENDPOINTS
# ============================================================

    def get_player_career_stats(
        self,
        player_id: int,
        group: str = "hitting",
    ) -> dict[str, Any]:
        return self._get(
            f"people/{player_id}/stats",
            params={
                "stats": "career",
                "group": group,
            },
        )


# ============================================================
# SECTION 16 - PLAYER YEAR-BY-YEAR STATS ENDPOINTS
# ============================================================

    def get_player_year_by_year_stats(
        self,
        player_id: int,
        group: str = "hitting",
    ) -> dict[str, Any]:
        return self._get(
            f"people/{player_id}/stats",
            params={
                "stats": "yearByYear",
                "group": group,
            },
        )


# ============================================================
# SECTION 17 - PLAYER SPLITS ENDPOINTS
# ============================================================

    def get_player_splits(
        self,
        player_id: int,
        season: int = 2026,
        group: str = "hitting",
        split: str = "homeAndAway",
    ) -> dict[str, Any]:
        return self._get(
            f"people/{player_id}/stats",
            params={
                "stats": split,
                "season": season,
                "group": group,
            },
        )


# ============================================================
# SECTION 18 - COMPLETE PLAYER PROFILE BUNDLE
# ============================================================

    def get_complete_player_profile(
        self,
        player_id: int,
        season: int = 2026,
    ) -> dict[str, Any]:
        return {
            "player": self.get_player(
                player_id=player_id,
            ),
            "season_hitting": self.get_player_season_stats(
                player_id=player_id,
                season=season,
                group="hitting",
            ),
            "season_pitching": self.get_player_season_stats(
                player_id=player_id,
                season=season,
                group="pitching",
            ),
            "season_fielding": self.get_player_season_stats(
                player_id=player_id,
                season=season,
                group="fielding",
            ),
            "career_hitting": self.get_player_career_stats(
                player_id=player_id,
                group="hitting",
            ),
            "career_pitching": self.get_player_career_stats(
                player_id=player_id,
                group="pitching",
            ),
            "career_fielding": self.get_player_career_stats(
                player_id=player_id,
                group="fielding",
            ),
            "game_log_hitting": self.get_player_game_log(
                player_id=player_id,
                season=season,
                group="hitting",
            ),
            "game_log_pitching": self.get_player_game_log(
                player_id=player_id,
                season=season,
                group="pitching",
            ),
        }


# ============================================================
# SECTION 19 - TEAM ROSTER COLLECTION HELPERS
# ============================================================

    def get_all_team_rosters(
        self,
        season: int = 2026,
        roster_type: str = "active",
    ) -> list[dict[str, Any]]:
        teams = self.get_teams(
            season=season,
        )

        all_rosters: list[dict[str, Any]] = []

        for team in teams:
            team_id = team.get("id")

            if not team_id:
                continue

            try:
                roster = self.get_roster(
                    team_id=team_id,
                    season=season,
                    roster_type=roster_type,
                )

                all_rosters.append(
                    {
                        "team": team,
                        "roster_type": roster_type,
                        "players": roster,
                    }
                )

            except Exception:
                continue

        return all_rosters


# ============================================================
# SECTION 20 - TEAM MULTI-ROSTER COLLECTION HELPERS
# ============================================================

    def get_all_roster_types_for_team(
        self,
        team_id: int,
        season: int = 2026,
    ) -> dict[str, Any]:
        roster_types = [
            "active",
            "40Man",
            "fullSeason",
            "depthChart",
            "nonRosterInvitees",
        ]

        result: dict[str, Any] = {
            "team_id": team_id,
            "season": season,
            "rosters": {},
        }

        for roster_type in roster_types:
            try:
                result["rosters"][roster_type] = self.get_roster(
                    team_id=team_id,
                    season=season,
                    roster_type=roster_type,
                )

            except Exception:
                result["rosters"][roster_type] = []

        return result


# ============================================================
# SECTION 21 - TEAM DEPTH CHART ENDPOINTS
# ============================================================

    def get_team_depth_chart(
        self,
        team_id: int,
        season: int = 2026,
    ) -> dict[str, Any]:
        return self._get(
            f"teams/{team_id}",
            params={
                "season": season,
                "hydrate": "depthChart",
            },
        )


# ============================================================
# SECTION 22 - TEAM FULL PROFILE ENDPOINTS
# ============================================================

    def get_team_full_profile(
        self,
        team_id: int,
        season: int = 2026,
    ) -> dict[str, Any]:
        return self._get(
            f"teams/{team_id}",
            params={
                "season": season,
                "hydrate": (
                    "venue,division,league,sport,leagueRecord,"
                    "records,probablePitcher,stats"
                ),
            },
        )


# ============================================================
# SECTION 23 - SCHEDULE GAME COLLECTION HELPERS
# ============================================================

    def get_schedule_games(
        self,
        season: int = 2026,
        start_date: str | None = None,
        end_date: str | None = None,
        team_id: int | None = None,
    ) -> list[dict[str, Any]]:
        payload = self.get_schedule(
            season=season,
            start_date=start_date,
            end_date=end_date,
            team_id=team_id,
        )

        games: list[dict[str, Any]] = []

        for date_block in payload.get("dates", []):
            for game in date_block.get("games", []):
                games.append(game)

        return games


# ============================================================
# SECTION 24 - GAME BOX SCORE ENDPOINTS
# ============================================================

    def get_game_boxscore(
        self,
        game_pk: int,
    ) -> dict[str, Any]:
        return self._get(
            f"game/{game_pk}/boxscore",
        )


# ============================================================
# SECTION 25 - GAME LINESCORE ENDPOINTS
# ============================================================

    def get_game_linescore(
        self,
        game_pk: int,
    ) -> dict[str, Any]:
        return self._get(
            f"game/{game_pk}/linescore",
        )


# ============================================================
# SECTION 26 - GAME CONTENT ENDPOINTS
# ============================================================

    def get_game_content(
        self,
        game_pk: int,
    ) -> dict[str, Any]:
        return self._get(
            f"game/{game_pk}/content",
        )


# ============================================================
# SECTION 27 - DIVISIONS ENDPOINTS
# ============================================================

    def get_divisions(
        self,
        sport_id: int = 1,
    ) -> list[dict[str, Any]]:
        payload = self._get(
            "divisions",
            params={
                "sportId": sport_id,
            },
        )

        return payload.get(
            "divisions",
            [],
        )


# ============================================================
# SECTION 28 - LEAGUES ENDPOINTS
# ============================================================

    def get_leagues(
        self,
        sport_id: int = 1,
    ) -> list[dict[str, Any]]:
        payload = self._get(
            "league",
            params={
                "sportId": sport_id,
            },
        )

        return payload.get(
            "leagues",
            [],
        )


# ============================================================
# SECTION 29 - VENUES ENDPOINTS
# ============================================================

    def get_venues(
        self,
    ) -> list[dict[str, Any]]:
        payload = self._get(
            "venues",
        )

        return payload.get(
            "venues",
            [],
        )


# ============================================================
# SECTION 30 - AWARDS ENDPOINTS
# ============================================================

    def get_awards(
        self,
        award_id: str | None = None,
        season: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}

        if award_id:
            params["awardId"] = award_id

        if season:
            params["season"] = season

        return self._get(
            "awards",
            params=params,
        )


# ============================================================
# SECTION 31 - PLAYER AWARDS ENDPOINTS
# ============================================================

    def get_player_awards(
        self,
        player_id: int,
    ) -> dict[str, Any]:
        return self._get(
            f"people/{player_id}/awards",
        )


# ============================================================
# SECTION 32 - DRAFT ENDPOINTS
# ============================================================

    def get_draft(
        self,
        year: int,
    ) -> dict[str, Any]:
        return self._get(
            f"draft/{year}",
        )


# ============================================================
# SECTION 33 - PROSPECTS ENDPOINTS
# ============================================================

    def get_prospects(
        self,
        sport_id: int = 1,
    ) -> dict[str, Any]:
        return self._get(
            "prospects",
            params={
                "sportId": sport_id,
            },
        )


# ============================================================
# SECTION 34 - PLAYER SEARCH BY ID LIST
# ============================================================

    def get_players_by_ids(
        self,
        player_ids: list[int],
    ) -> list[dict[str, Any]]:
        players: list[dict[str, Any]] = []

        for player_id in player_ids:
            try:
                player = self.get_player(
                    player_id=player_id,
                )

                if player:
                    players.append(player)

            except Exception:
                continue

        return players

# ============================================================
# SECTION 35 - BASEBALL SAVANT / STATCAST INTEGRATION
# ============================================================

    def get_statcast_range(
        self,
        start_date: str,
        end_date: str,
    ):
        """
        Pull all Statcast events between dates.

        Example:
        2025-04-01
        2025-04-07
        """

        return statcast(
            start_dt=start_date,
            end_dt=end_date,
        )


# ============================================================
# SECTION 35A - BATTER STATCAST DATA
# ============================================================

    def get_statcast_batter(
        self,
        player_id: int,
        start_date: str,
        end_date: str,
    ):
        """
        Batter-level Statcast data.
        """

        return statcast_batter(
            start_dt=start_date,
            end_dt=end_date,
            player_id=player_id,
        )


# ============================================================
# SECTION 35B - PITCHER STATCAST DATA
# ============================================================

    def get_statcast_pitcher(
        self,
        player_id: int,
        start_date: str,
        end_date: str,
    ):
        """
        Pitcher-level Statcast data.
        """

        return statcast_pitcher(
            start_dt=start_date,
            end_dt=end_date,
            player_id=player_id,
        )


# ============================================================
# SECTION 35C - DAILY STATCAST INGESTION
# ============================================================

    def get_daily_statcast_update(
        self,
        target_date: str,
    ):
        """
        Single-day Statcast update.

        Intended for future automated syncs.
        """

        return statcast(
            start_dt=target_date,
            end_dt=target_date,
        )


# ============================================================
# SECTION 35D - PLAYER STATCAST PROFILE
# ============================================================

    def get_statcast_player_profile(
        self,
        player_id: int,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        return {
            "batter_events": self.get_statcast_batter(
                player_id=player_id,
                start_date=start_date,
                end_date=end_date,
            ),
            "pitcher_events": self.get_statcast_pitcher(
                player_id=player_id,
                start_date=start_date,
                end_date=end_date,
            ),
        }
# ============================================================
# SECTION 36 - FUTURE DATA SOURCE ROADMAP
# ============================================================

"""
Future MLBStatsAPIClient Expansion

1. Injury endpoint discovery
2. Lineup endpoint discovery
3. Probable pitcher hydration
4. Weather source integration
5. Baseball Savant CSV ingestion
6. FanGraphs leaderboards
7. Lahman historical database
8. Retrosheet play-by-play
9. Minor league player sync
10. Prospect rankings
11. Park factor ingestion
12. Betting odds provider integration
13. DFS salary provider integration
14. Daily scheduled data refresh
"""