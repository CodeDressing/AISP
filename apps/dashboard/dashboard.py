# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 4.00 PART 1
# ENTERPRISE AI SPORTS COMMAND CENTER
# FILE: apps/dashboard/dashboard.py
# PURPOSE: premium AI-driven frontend experience for MLB analytics,
# player intelligence, predictions, AI assistant workflows,
# warehouse monitoring, and enterprise sports intelligence
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st


# ============================================================
# SECTION 02 - APPLICATION CONFIGURATION
# ============================================================

DEFAULT_LOCAL_API = "http://127.0.0.1:8000"

API_BASE = os.getenv(
    "AISP_API_BASE_URL",
    DEFAULT_LOCAL_API,
)

st.set_page_config(
    page_title="AISP Command Center",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SECTION 03 - API HELPERS
# ============================================================

def api_get(
    path: str,
    params: dict[str, Any] | None = None,
    timeout: int = 20,
) -> dict | list | None:
    try:
        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"API GET failed: {exc}")
        return None


def api_post(
    path: str,
    payload: dict[str, Any],
    timeout: int = 30,
) -> dict | list | None:
    try:
        response = requests.post(
            f"{API_BASE}{path}",
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"API POST failed: {exc}")
        return None


# ============================================================
# SECTION 04 - ENTERPRISE AI DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37,99,235,0.28), transparent 32%),
                radial-gradient(circle at top right, rgba(14,165,233,0.18), transparent 28%),
                linear-gradient(180deg, #020617 0%, #0B1120 48%, #111827 100%);
            color: #F8FAFC;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #020617 0%, #0F172A 100%);
            border-right: 1px solid rgba(148,163,184,0.20);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .hero-panel {
            background:
                linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.76)),
                radial-gradient(circle at top right, rgba(56,189,248,0.35), transparent 35%);
            border: 1px solid rgba(148,163,184,0.22);
            border-radius: 28px;
            padding: 38px;
            margin-bottom: 24px;
            box-shadow: 0 24px 80px rgba(0,0,0,0.35);
        }

        .main-title {
            font-size: 54px;
            font-weight: 950;
            letter-spacing: -1.8px;
            color: #FFFFFF;
            margin-bottom: 4px;
        }

        .main-subtitle {
            font-size: 18px;
            color: #CBD5E1;
            max-width: 950px;
        }

        .pill-row {
            margin-top: 22px;
        }

        .pill {
            display: inline-block;
            padding: 8px 14px;
            border-radius: 999px;
            margin-right: 8px;
            margin-bottom: 8px;
            background: rgba(15,23,42,0.78);
            border: 1px solid rgba(148,163,184,0.25);
            color: #E2E8F0;
            font-size: 13px;
            font-weight: 700;
        }

        .glass-card {
            background: rgba(15,23,42,0.76);
            border: 1px solid rgba(148,163,184,0.22);
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 14px 45px rgba(0,0,0,0.25);
            min-height: 140px;
        }

        .glass-card h3 {
            color: #FFFFFF;
            margin-bottom: 8px;
            font-size: 21px;
        }

        .glass-card p {
            color: #CBD5E1;
            font-size: 14px;
            line-height: 1.55;
        }

        .ai-card {
            background:
                linear-gradient(145deg, rgba(8,47,73,0.88), rgba(15,23,42,0.90));
            border: 1px solid rgba(56,189,248,0.28);
            border-radius: 24px;
            padding: 26px;
            box-shadow: 0 18px 55px rgba(14,165,233,0.12);
        }

        .metric-label {
            color: #94A3B8;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .metric-value {
            color: #F8FAFC;
            font-size: 34px;
            font-weight: 900;
            margin-top: 4px;
        }

        .metric-note {
            color: #94A3B8;
            font-size: 13px;
            margin-top: 4px;
        }

        .status-good {
            color: #22C55E;
            font-weight: 900;
        }

        .status-warn {
            color: #F59E0B;
            font-weight: 900;
        }

        .status-bad {
            color: #EF4444;
            font-weight: 900;
        }

        .section-kicker {
            color: #38BDF8;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-size: 12px;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .section-heading {
            font-size: 31px;
            font-weight: 900;
            color: #FFFFFF;
            margin-bottom: 14px;
        }

        .dataframe {
            border-radius: 14px;
        }

        div[data-testid="stMetric"] {
            background: rgba(15,23,42,0.62);
            border: 1px solid rgba(148,163,184,0.18);
            padding: 18px;
            border-radius: 18px;
        }

        .footer-note {
            color: #64748B;
            font-size: 13px;
            text-align: center;
            padding-top: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SECTION 05 - SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown("## ⚾ AISP")
st.sidebar.caption("AI Sports Command Center")

page = st.sidebar.radio(
    "Navigation",
    [
        "Command Center",
        "Players",
        "Teams",
        "Games",
        "Predictions",
        "AI Analyst",
        "Analytics",
        "Warehouse",
        "System Health",
    ],
)

st.sidebar.divider()

api_override = st.sidebar.text_input(
    "API Base URL",
    value=API_BASE,
)

if api_override:
    API_BASE = api_override.rstrip("/")

st.sidebar.divider()
st.sidebar.caption("Phase 4.00 Enterprise AI Aesthetic")


# ============================================================
# SECTION 06 - SHARED UI HELPERS
# ============================================================

def render_header(
    title: str,
    subtitle: str,
    pills: list[str] | None = None,
) -> None:
    pill_html = ""

    if pills:
        pill_html = "<div class='pill-row'>"
        for pill in pills:
            pill_html += f"<span class='pill'>{pill}</span>"
        pill_html += "</div>"

    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="main-title">{title}</div>
            <div class="main-subtitle">{subtitle}</div>
            {pill_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_glass_card(
    title: str,
    body: str,
) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(
    label: str,
    value: str,
    note: str,
) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SECTION 07 - COMMAND CENTER HOME
# ============================================================

def render_command_center() -> None:
    render_header(
        "AISP Command Center",
        "Live MLB warehouse status, Baseball Savant connectivity, prediction readiness, and AI sports intelligence controls.",
        [
            "Live Warehouse",
            "Baseball Savant",
            "Statcast",
            "ML Pipeline",
            "AI Analyst",
        ],
    )

    health = api_get("/health", timeout=5)
    summary = api_get("/admin/database/summary", timeout=10)
    readiness = api_get("/admin/platform/readiness", timeout=10)
    sources = api_get("/admin/data-sources/status", timeout=10)

    api_online = bool(health)
    database_online = bool(
        isinstance(health, dict)
        and health.get("database")
    )

    teams_loaded = 0
    players_loaded = 0
    games_loaded = 0
    predictions_loaded = 0

    if isinstance(summary, dict):
        teams_loaded = summary.get("teams", 0)
        players_loaded = summary.get("players", 0)
        games_loaded = summary.get("games", 0)
        predictions_loaded = (
            summary.get("game_predictions", 0)
            + summary.get("player_predictions", 0)
        )

    readiness_score = 0

    if isinstance(readiness, dict):
        readiness_score = readiness.get("readiness_score", 0)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_metric_card(
            "API Status",
            "ONLINE" if api_online else "OFFLINE",
            "FastAPI backend connection",
        )

    with c2:
        render_metric_card(
            "Database",
            "ONLINE" if database_online else "CHECK",
            "Warehouse connection status",
        )

    with c3:
        render_metric_card(
            "Players Loaded",
            f"{players_loaded:,}",
            "Current player records",
        )

    with c4:
        render_metric_card(
            "Readiness",
            f"{readiness_score}/100",
            "Enterprise platform score",
        )

    st.divider()

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        render_metric_card(
            "Teams",
            f"{teams_loaded:,}",
            "MLB teams stored",
        )

    with k2:
        render_metric_card(
            "Games",
            f"{games_loaded:,}",
            "Stored game records",
        )

    with k3:
        render_metric_card(
            "Predictions",
            f"{predictions_loaded:,}",
            "Game + player predictions",
        )

    with k4:
        statcast_status = "UNKNOWN"

        if isinstance(sources, dict):
            statcast_status = (
                "CONNECTED"
                if sources.get("baseball_savant")
                else "OFFLINE"
            )

        render_metric_card(
            "Statcast",
            statcast_status,
            "Baseball Savant data source",
        )

    st.divider()

    st.markdown(
        "<div class='section-kicker'>Live Baseball Savant Test</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='section-heading'>Statcast Connection</div>",
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns([1, 1, 1])

    with s1:
        start_date = st.text_input(
            "Sample Start Date",
            value="2025-04-01",
            key="home_statcast_start",
        )

    with s2:
        end_date = st.text_input(
            "Sample End Date",
            value="2025-04-02",
            key="home_statcast_end",
        )

    with s3:
        st.write("")
        st.write("")
        run_sample = st.button(
            "Test Statcast",
            use_container_width=True,
        )

    if run_sample:
        data = api_get(
            "/admin/statcast/sample",
            params={
                "start_date": start_date,
                "end_date": end_date,
            },
            timeout=120,
        )

        if data:
            result = data.get("result", {})

            r1, r2, r3 = st.columns(3)

            with r1:
                st.metric(
                    "Rows Returned",
                    result.get("rows", 0),
                )

            with r2:
                st.metric(
                    "Columns",
                    result.get("columns", 0),
                )

            with r3:
                st.metric(
                    "Source",
                    "Baseball Savant",
                )

            st.json(data)

    st.divider()

    st.markdown(
        "<div class='section-kicker'>Command Modules</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='section-heading'>Enterprise Sports Intelligence</div>",
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        render_glass_card(
            "Player Intelligence",
            "Search players, inspect MLB profiles, load Statcast context, and prepare player prop models.",
        )

    with m2:
        render_glass_card(
            "Prediction Workbench",
            "Use feature engineering, simulation logic, and future neural network models for MLB predictions.",
        )

    with m3:
        render_glass_card(
            "AI Analyst",
            "Ask natural language questions and route them into database-aware baseball intelligence.",
        )

    st.divider()

    st.markdown(
        "<div class='section-kicker'>System Controls</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='section-heading'>Operations</div>",
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("Run Health Check", use_container_width=True):
            st.json(api_get("/health"))

    with q2:
        if st.button("View API Routes", use_container_width=True):
            st.json(api_get("/system/routes"))

    with q3:
        if st.button("Database Summary", use_container_width=True):
            st.json(api_get("/admin/database/summary"))
# ============================================================
# SECTION 08 - PLAYERS PAGE
# ============================================================

def render_players_page() -> None:
    render_header(
        "Player Intelligence",
        "Search every stored MLB player and prepare player cards, projections, and AI-generated analysis.",
        ["Player Search", "Stats", "Props", "Profiles"],
    )

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Search Player Database")

        query = st.text_input(
            "Player Name",
            value="Juan Soto",
        )

        if st.button("Search Players", use_container_width=True):
            data = api_get(
                "/players/search",
                params={"q": query},
            )

            if data:
                st.dataframe(
                    data,
                    use_container_width=True,
                )

    with right:
        st.markdown(
            """
            <div class="ai-card">
                <h3>AI Player Lens</h3>
                <p>Use this workspace to identify players, inspect database results, and prepare future player cards with probability gauges.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Player Detail Lookup")

    player_id = st.number_input(
        "MLB Player ID",
        value=660271,
        step=1,
    )

    if st.button("Load Player Detail", use_container_width=True):
        data = api_get(
            f"/players/{int(player_id)}",
        )

        if data:
            st.json(data)


# ============================================================
# SECTION 09 - TEAMS PAGE
# ============================================================

def render_teams_page() -> None:
    render_header(
        "Team Intelligence",
        "Explore MLB teams, divisions, rosters, venues, and future strength ratings.",
        ["Teams", "Rosters", "Divisions", "Strength Ratings"],
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Load All Teams", use_container_width=True):
            data = api_get("/teams")

            if data:
                st.dataframe(
                    data,
                    use_container_width=True,
                )

    with col2:
        team_id = st.number_input(
            "Team ID",
            value=147,
            step=1,
        )

        if st.button("Load Team Detail", use_container_width=True):
            data = api_get(f"/teams/{int(team_id)}")

            if data:
                st.json(data)


# ============================================================
# SECTION 10 - GAMES PAGE
# ============================================================

def render_games_page() -> None:
    render_header(
        "Game Intelligence",
        "Stored game records, matchup research, score context, and future win probability workflows.",
        ["Games", "Matchups", "Scores", "Win Probability"],
    )

    limit = st.slider(
        "Number of games",
        min_value=10,
        max_value=500,
        value=100,
    )

    if st.button("Load Games", use_container_width=True):
        data = api_get(
            "/games",
            params={"limit": limit},
        )

        if data:
            st.dataframe(
                data,
                use_container_width=True,
            )


# ============================================================
# SECTION 11 - HUMAN-FRIENDLY PROBABILITY VIEWER
# ============================================================

def render_predictions_page() -> None:
    render_header(
        "AISP Probability Viewer",
        "Choose a team, choose a player, select a baseball outcome in plain English, and prepare a prediction.",
        [
            "Plain English Team List",
            "Plain English Player Search",
            "Hits",
            "Home Runs",
            "Doubles",
            "Triples",
            "Probability Viewer",
        ],
    )

    summary = api_get(
        "/admin/database/summary",
        timeout=20,
    )

    if summary:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Teams Available",
                summary.get("teams", 0),
            )

        with c2:
            st.metric(
                "Players Available",
                summary.get("players", 0),
            )

        with c3:
            st.metric(
                "Statcast Events",
                summary.get("statcast_events", 0),
            )

    st.divider()

    teams = api_get(
        "/teams",
        timeout=20,
    )

    if not teams:
        st.error(
            "No teams are visible yet. Go to Warehouse and run Sync Teams first."
        )
        return

    team_options = {
        team.get("name", "Unknown Team"): team
        for team in teams
    }

    st.subheader("Step 1 — Choose A Team")

    selected_team_name = st.selectbox(
        "Team",
        list(team_options.keys()),
        help="Choose one MLB team from a regular English list.",
    )

    selected_team = team_options[selected_team_name]

    st.success(
        f"You selected: {selected_team_name}"
    )

    with st.expander("View selected team details"):
        st.write(f"Team: {selected_team.get('name')}")
        st.write(f"Abbreviation: {selected_team.get('abbreviation')}")
        st.write(f"League: {selected_team.get('league')}")
        st.write(f"Division: {selected_team.get('division')}")
        st.write(f"Home Ballpark: {selected_team.get('venue')}")

    st.divider()

    st.subheader("Step 2 — Find A Player")

    player_search = st.text_input(
        "Type a player name",
        value="Corbin Carroll",
        help="Example: Corbin Carroll, Aaron Judge, Shohei Ohtani, Juan Soto",
    )

    if st.button(
        "Search Players",
        use_container_width=True,
    ):
        players = api_get(
            "/players/search",
            params={
                "q": player_search,
            },
            timeout=20,
        )

        if players:
            st.session_state["probability_player_results"] = players
            st.success(
                f"Found {len(players)} player result(s)."
            )
        else:
            st.warning(
                "No players found. If this keeps happening, go to Warehouse and run Sync Rosters / Players."
            )

    player_results = st.session_state.get(
        "probability_player_results",
        [],
    )

    selected_player = None

    if player_results:
        player_options = {
            (
                f"{player.get('name', 'Unknown Player')}"
                f" — {player.get('team', 'Unknown Team')}"
                f" — {player.get('position', 'Unknown Position')}"
            ): player
            for player in player_results
        }

        selected_player_label = st.selectbox(
            "Choose Player",
            list(player_options.keys()),
        )

        selected_player = player_options[selected_player_label]

        with st.expander("View selected player details"):
            st.write(f"Player: {selected_player.get('name')}")
            st.write(f"Team: {selected_player.get('team')}")
            st.write(f"Position: {selected_player.get('position')}")
            st.write(f"Bats: {selected_player.get('bats')}")
            st.write(f"Throws: {selected_player.get('throws')}")
            st.write(f"Height: {selected_player.get('height')}")
            st.write(f"Weight: {selected_player.get('weight')}")

    st.divider()

    st.subheader("Step 3 — Choose What You Want To Predict")

    outcome = st.selectbox(
        "Outcome",
        [
            "Gets at least 1 hit",
            "Hits a single",
            "Hits a double",
            "Hits a triple",
            "Hits a home run",
            "Gets an RBI",
            "Scores a run",
            "Walks",
            "Strikes out",
            "Steals a base",
            "Over 0.5 total bases",
            "Over 1.5 total bases",
            "Over 2.5 total bases",
        ],
    )

    game_context = st.selectbox(
        "Game Context",
        [
            "Any upcoming game",
            "Home game",
            "Away game",
            "Against selected opponent",
        ],
    )

    opponent_name = None

    if game_context == "Against selected opponent":
        opponent_name = st.selectbox(
            "Opponent Team",
            list(team_options.keys()),
        )

    st.divider()

    st.subheader("Step 4 — Probability Viewer")

    if st.button(
        "Prepare Probability Prediction",
        use_container_width=True,
    ):
        if not selected_player:
            st.error(
                "Please search for and select a player first."
            )
            return

        st.success(
            "Prediction setup is ready."
        )

        st.markdown("### Plain English Summary")

        st.write(
            f"Team: **{selected_team_name}**"
        )

        st.write(
            f"Player: **{selected_player.get('name')}**"
        )

        st.write(
            f"Outcome to predict: **{outcome}**"
        )

        if opponent_name:
            st.write(
                f"Opponent: **{opponent_name}**"
            )

        st.info(
            "This screen is now ready for the backend prediction endpoint. Next upgrade will connect this setup to `/predict/player` and return a real probability."
        )

        st.markdown("### Future Probability Output")

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                "Estimated Probability",
                "Pending Model",
            )

        with p2:
            st.metric(
                "Confidence",
                "Pending Model",
            )

        with p3:
            st.metric(
                "Model",
                "AISP Baseline",
            )

        st.json(
            {
                "team": selected_team,
                "player": selected_player,
                "outcome": outcome,
                "game_context": game_context,
                "opponent": opponent_name,
                "next_backend_endpoint": "/predict/player",
                "future_result_example": {
                    "probability": "0.00 to 1.00",
                    "confidence": "0.00 to 1.00",
                    "reasoning": [
                        "recent player stats",
                        "team context",
                        "opponent matchup",
                        "park factors",
                        "Statcast trends",
                    ],
                },
            }
        )
# ============================================================
# SECTION 12 - AI ANALYST PAGE
# ============================================================

def render_ai_analyst_page() -> None:
    render_header(
        "AISP AI Analyst",
        "Ask baseball questions in natural language and receive structured database-aware responses.",
        ["Natural Language", "Database Lookup", "Predictions", "Explanations"],
    )

    left, right = st.columns([2, 1])

    with left:
        message = st.text_area(
            "Ask AISP",
            value="Predict Juan Soto hit probability",
            height=190,
        )

        if st.button("Ask AI Analyst", use_container_width=True):
            data = api_post(
                "/chat",
                payload={"message": message},
            )

            if data:
                st.json(data)

    with right:
        render_glass_card(
            "Example Prompts",
            "Try: Show me Juan Soto stats. Predict Aaron Judge hit probability. Show me Yankees roster. Who are the OPS leaders?",
        )


# ============================================================
# SECTION 13 - ANALYTICS PAGE
# ============================================================

def render_analytics_page() -> None:

    render_header(
        "Baseball Intelligence Center",
        "Live Statcast, warehouse analytics, data source monitoring, and future machine learning insights.",
        [
            "Statcast",
            "Baseball Savant",
            "ML Models",
            "Predictions",
            "Warehouse",
        ],
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Statcast",
            "Data Sources",
            "ML Pipeline",
            "Warehouse",
        ]
    )

    # ========================================================
    # TAB 1 - STATCAST
    # ========================================================

    with tab1:

        st.subheader(
            "⚾ Baseball Savant / Statcast"
        )

        c1, c2 = st.columns(2)

        with c1:
            start_date = st.text_input(
                "Start Date",
                value="2025-04-01",
            )

        with c2:
            end_date = st.text_input(
                "End Date",
                value="2025-04-02",
            )

        if st.button(
            "Pull Statcast Sample",
            use_container_width=True,
        ):

            data = api_get(
                "/admin/statcast/sample",
                params={
                    "start_date": start_date,
                    "end_date": end_date,
                },
                timeout=120,
            )

            if data:
                st.success(
                    "Statcast connection successful"
                )

                st.json(data)

        st.divider()

        player_id = st.number_input(
            "Player ID",
            value=660271,
            step=1,
        )

        if st.button(
            "Load Player Statcast Profile",
            use_container_width=True,
        ):

            data = api_get(
                f"/admin/statcast/player/{int(player_id)}",
                params={
                    "start_date": start_date,
                    "end_date": end_date,
                },
                timeout=120,
            )

            if data:
                st.json(data)

    # ========================================================
    # TAB 2 - DATA SOURCES
    # ========================================================

    with tab2:

        st.subheader(
            "Connected Data Sources"
        )

        status = api_get(
            "/admin/data-sources/status"
        )

        if status:
            st.json(status)

    # ========================================================
    # TAB 3 - MACHINE LEARNING
    # ========================================================

    with tab3:

        st.subheader(
            "AISP Neural Network Roadmap"
        )

        st.code(
            """
Input Layer
│
├── Player Features
├── Team Features
├── Statcast Features
├── Injury Features
├── Weather Features
├── Betting Features
│
Hidden Layer 1 (256)
Hidden Layer 2 (128)
Hidden Layer 3 (64)
│
Output Layer
├── Win Probability
├── Hit Probability
├── HR Probability
├── Strikeout Probability
├── Player Props
            """
        )

        st.info(
            "Current Phase: Feature Engineering Foundation"
        )

    # ========================================================
    # TAB 4 - WAREHOUSE
    # ========================================================

    with tab4:

        summary = api_get(
            "/admin/database/summary"
        )

        if summary:
            st.json(summary)
# ============================================================
# SECTION 14 - WAREHOUSE COMMAND CENTER
# ============================================================

def render_warehouse_page() -> None:

    render_header(
        "AISP Warehouse Control Room",
        "This is where you can see what data exists, sync new data, view teams, search players, and verify progress.",
        [
            "Data Progress",
            "Sync Controls",
            "Teams Viewer",
            "Players Viewer",
            "Prediction Readiness",
        ],
    )

    summary = api_get(
        "/admin/database/summary",
        timeout=20,
    )

    audit = api_get(
        "/admin/warehouse/audit",
        timeout=20,
    )

    if not summary:
        st.error(
            "Unable to load database summary. Check API connection."
        )
        return

    st.subheader("Current Database Counts")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("Teams", summary.get("teams", 0))

    with c2:
        st.metric("Players", summary.get("players", 0))

    with c3:
        st.metric("Games", summary.get("games", 0))

    with c4:
        st.metric(
            "Predictions",
            summary.get("game_predictions", 0)
            + summary.get("player_predictions", 0),
        )

    with c5:
        st.metric("Statcast", summary.get("statcast_events", 0))

    st.divider()

    st.subheader("Warehouse Audit")

    if audit:
        score = audit.get("warehouse_score", 0)
        st.progress(score / 100)
        st.write(f"Warehouse Score: {score}/100")
        st.json(audit)
    else:
        st.warning("Warehouse audit endpoint is not available yet.")

    st.divider()

    st.subheader("Sync Data Into AISP")

    season = st.number_input(
        "Season",
        value=2026,
        step=1,
    )

    s1, s2, s3 = st.columns(3)

    with s1:
        if st.button("1. Sync Teams", use_container_width=True):
            result = api_post(
                f"/admin/sync/teams?season={int(season)}",
                payload={},
                timeout=120,
            )

            if result:
                st.success("Teams sync finished.")
                st.json(result)

    with s2:
        if st.button("2. Sync Rosters / Players", use_container_width=True):
            result = api_post(
                f"/admin/sync/rosters?season={int(season)}",
                payload={},
                timeout=300,
            )

            if result:
                st.success("Roster sync finished.")
                st.json(result)

    with s3:
        if st.button("3. Full MLB Sync", use_container_width=True):
            result = api_post(
                f"/admin/sync/mlb?season={int(season)}",
                payload={},
                timeout=600,
            )

            if result:
                st.success("Full MLB sync finished.")
                st.json(result)

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "View Teams",
            "Search Players",
            "Raw System Data",
        ]
    )

    with tab1:
        st.subheader("All Teams In Database")

        teams = api_get(
            "/teams",
            timeout=20,
        )

        if teams:
            st.success(f"{len(teams)} teams found.")
            st.dataframe(
                teams,
                use_container_width=True,
            )

            team_options = {
                f"{team.get('name')} ({team.get('abbreviation')})": team
                for team in teams
            }

            selected_team_label = st.selectbox(
                "Select Team",
                list(team_options.keys()),
            )

            st.json(
                team_options[selected_team_label]
            )

        else:
            st.warning(
                "No teams found. Click 'Sync Teams' above first."
            )

    with tab2:
        st.subheader("Search Players In Database")

        player_search = st.text_input(
            "Player Search",
            value="Judge",
        )

        if st.button("Search Players", use_container_width=True):
            players = api_get(
                "/players/search",
                params={
                    "q": player_search,
                },
                timeout=20,
            )

            if players:
                st.success(f"{len(players)} player results found.")
                st.dataframe(
                    players,
                    use_container_width=True,
                )

                player_options = {
                    f"{player.get('name')} | {player.get('team')} | {player.get('position')}": player
                    for player in players
                }

                selected_player_label = st.selectbox(
                    "Select Player",
                    list(player_options.keys()),
                )

                st.json(
                    player_options[selected_player_label]
                )

            else:
                st.warning(
                    "No players found. Click 'Sync Rosters / Players' first."
                )

    with tab3:
        st.subheader("Raw Warehouse Snapshot")

        st.json(summary)

        if audit:
            st.json(audit)
# ============================================================
# SECTION 15 - SYSTEM HEALTH PAGE
# ============================================================

def render_system_health_page() -> None:
    render_header(
        "System Health",
        "Monitor Render deployment, API routes, database connectivity, and backend readiness.",
        ["Render", "FastAPI", "Database", "Routes"],
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Health")
        data = api_get("/health")
        if data:
            st.json(data)

    with col2:
        st.subheader("Database")
        data = api_get("/health/database")
        if data:
            st.json(data)

    st.divider()

    st.subheader("Routes")

    routes = api_get("/system/routes")

    if routes:
        st.json(routes)


# ============================================================
# SECTION 16 - PAGE ROUTER
# ============================================================

if page == "Command Center":
    render_command_center()

elif page == "Players":
    render_players_page()

elif page == "Teams":
    render_teams_page()

elif page == "Games":
    render_games_page()

elif page == "Predictions":
    render_predictions_page()

elif page == "AI Analyst":
    render_ai_analyst_page()

elif page == "Analytics":
    render_analytics_page()

elif page == "Warehouse":
    render_warehouse_page()

elif page == "System Health":
    render_system_health_page()


# ============================================================
# SECTION 17 - FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer-note">
        AISP Baseball Analytics Engine · Enterprise AI Sports Intelligence · Phase 4.00
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SECTION 18 - FUTURE FRONTEND ROADMAP
# ============================================================

"""
Phase 4.01

Player cards
Team cards
Leaderboards
Statcast visuals
Prediction confidence meters
Charts
Filters
AI response formatting

Phase 4.02

Frontend deployment on Render

Phase 4.03

Dedicated React / Next.js web application

Phase 5.00

Sportsbook Intelligence UI
"""