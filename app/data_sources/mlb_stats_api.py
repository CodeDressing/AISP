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