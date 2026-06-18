# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 3.11 PART 1
# ENTERPRISE STREAMLIT DASHBOARD PLATFORM
# FILE: apps/dashboard/dashboard.py
# PURPOSE: enterprise visual frontend for MLB analytics,
# player search, team intelligence, predictions, AI chat,
# warehouse monitoring, and system health
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
    page_title="AISP Baseball Analytics",
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
# SECTION 04 - ENTERPRISE STYLING
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #050816 0%, #0E1117 100%);
            color: #F8FAFC;
        }

        .main-title {
            font-size: 48px;
            font-weight: 900;
            color: #FFFFFF;
            margin-bottom: 0px;
        }

        .main-subtitle {
            font-size: 18px;
            color: #CBD5E1;
            margin-bottom: 30px;
        }

        .section-title {
            font-size: 28px;
            font-weight: 800;
            color: #F8FAFC;
            margin-top: 16px;
            margin-bottom: 8px;
        }

        .aisp-card {
            background: #111827;
            border: 1px solid #1F2937;
            border-radius: 18px;
            padding: 22px;
            min-height: 120px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.20);
        }

        .aisp-card h3 {
            color: #FFFFFF;
            margin-bottom: 8px;
        }

        .aisp-card p {
            color: #CBD5E1;
            font-size: 15px;
        }

        .status-online {
            color: #22C55E;
            font-weight: 900;
        }

        .status-offline {
            color: #EF4444;
            font-weight: 900;
        }

        .small-muted {
            color: #94A3B8;
            font-size: 13px;
        }

        .hero-panel {
            background: radial-gradient(circle at top left, #1E3A8A 0%, #111827 45%, #020617 100%);
            border: 1px solid #1F2937;
            border-radius: 24px;
            padding: 36px;
            margin-bottom: 25px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SECTION 05 - SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("⚾ AISP")
st.sidebar.caption("Artificial Intelligence Sports Predictor")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Players",
        "Teams",
        "Games",
        "Predictions",
        "AI Assistant",
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

st.sidebar.caption("Phase 3.11 Enterprise Dashboard")


# ============================================================
# SECTION 06 - SHARED HEADER
# ============================================================

def render_header(
    title: str,
    subtitle: str,
) -> None:
    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="main-title">{title}</div>
            <div class="main-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SECTION 07 - DASHBOARD HOME
# ============================================================

def render_dashboard_home() -> None:
    render_header(
        "AISP Baseball Analytics",
        "Enterprise MLB intelligence, predictions, rosters, player analytics, and AI-assisted decision support.",
    )

    health = api_get("/health", timeout=5)

    api_online = bool(health)
    database_online = bool(
        isinstance(health, dict)
        and health.get("database")
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "API Status",
            "ONLINE" if api_online else "OFFLINE",
        )

    with c2:
        st.metric(
            "Database",
            "ONLINE" if database_online else "CHECK",
        )

    with c3:
        st.metric(
            "Sport",
            "MLB",
        )

    with c4:
        st.metric(
            "Platform Phase",
            "3.11",
        )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="aisp-card">
                <h3>MLB Database</h3>
                <p>Teams, players, rosters, season stats, games, and warehouse storage.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="aisp-card">
                <h3>Prediction Engine</h3>
                <p>Hit probability, game prediction, player props, and simulation framework.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="aisp-card">
                <h3>AI Assistant</h3>
                <p>Ask baseball questions and route them into analytics and prediction logic.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Quick Actions")

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("Check API Health", use_container_width=True):
            st.json(api_get("/health"))

    with q2:
        if st.button("View Routes", use_container_width=True):
            st.json(api_get("/system/routes"))

    with q3:
        if st.button("System Info", use_container_width=True):
            st.json(api_get("/system/info"))


# ============================================================
# SECTION 08 - PLAYERS WORKSPACE
# ============================================================

def render_players_page() -> None:
    render_header(
        "Players",
        "Search active MLB players, inspect team context, and prepare player-level predictions.",
    )

    query = st.text_input(
        "Search MLB Player",
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
# SECTION 09 - TEAMS WORKSPACE
# ============================================================

def render_teams_page() -> None:
    render_header(
        "Teams",
        "Explore MLB team records, roster data, divisions, and team identifiers.",
    )

    if st.button("Load All Teams", use_container_width=True):
        data = api_get("/teams")

        if data:
            st.dataframe(
                data,
                use_container_width=True,
            )

    st.divider()

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
# SECTION 10 - GAMES WORKSPACE
# ============================================================

def render_games_page() -> None:
    render_header(
        "Games",
        "View stored game records and prepare matchup prediction workflows.",
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
# SECTION 11 - PREDICTIONS WORKSPACE
# ============================================================

def render_predictions_page() -> None:
    render_header(
        "Predictions",
        "Review game predictions, player predictions, and future simulation outputs.",
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Game Predictions",
            "Player Predictions",
            "Prediction Lab",
        ]
    )

    with tab1:
        limit = st.slider(
            "Game prediction rows",
            10,
            250,
            100,
        )

        if st.button("Load Game Predictions", use_container_width=True):
            data = api_get(
                "/predictions/games",
                params={"limit": limit},
            )

            if data:
                st.dataframe(
                    data,
                    use_container_width=True,
                )

    with tab2:
        limit = st.slider(
            "Player prediction rows",
            10,
            250,
            100,
        )

        if st.button("Load Player Predictions", use_container_width=True):
            data = api_get(
                "/predictions/players",
                params={"limit": limit},
            )

            if data:
                st.dataframe(
                    data,
                    use_container_width=True,
                )

    with tab3:
        st.subheader("Prediction Lab")
        prediction_type = st.selectbox(
            "Prediction Type",
            [
                "Hit Probability",
                "Home Run Probability",
                "Game Winner",
                "Strikeout Probability",
                "Monte Carlo Simulation",
            ],
        )

        st.info(
            f"Selected model workspace: {prediction_type}"
        )


# ============================================================
# SECTION 12 - AI ASSISTANT WORKSPACE
# ============================================================

def render_ai_assistant_page() -> None:
    render_header(
        "AISP AI Assistant",
        "Ask natural language baseball questions and route them into AISP analytics.",
    )

    message = st.text_area(
        "Ask AISP",
        value="Predict Juan Soto hit probability",
        height=180,
    )

    if st.button("Ask AISP", use_container_width=True):
        data = api_post(
            "/chat",
            payload={"message": message},
        )

        if data:
            st.json(data)

    st.divider()

    st.caption("Example prompts")
    st.code("Show me Juan Soto stats")
    st.code("Predict Aaron Judge hit probability")
    st.code("Show me Yankees roster")
    st.code("Who are the OPS leaders?")


# ============================================================
# SECTION 13 - ANALYTICS CENTER
# ============================================================

def render_analytics_page() -> None:
    render_header(
        "Analytics Center",
        "A workspace for batting, pitching, Statcast, trends, and future charts.",
    )

    st.subheader("Analytics Modules")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Batting", "Planned")

    with col2:
        st.metric("Pitching", "Planned")

    with col3:
        st.metric("Fielding", "Planned")

    with col4:
        st.metric("Statcast", "Planned")

    st.warning(
        "Phase 3.12 will add charts, player comparison tables, and leaderboard views."
    )


# ============================================================
# SECTION 14 - WAREHOUSE MONITOR
# ============================================================

def render_warehouse_page() -> None:
    render_header(
        "Data Warehouse",
        "Monitor the current state of the local MLB database and future warehouse jobs.",
    )

    st.subheader("Warehouse Status")

    info = api_get("/system/info")

    if info:
        st.json(info)

    st.divider()

    st.info(
        "Upcoming: row counts, sync timestamps, table health, data quality scores, and nightly job status."
    )


# ============================================================
# SECTION 15 - SYSTEM HEALTH
# ============================================================

def render_system_health_page() -> None:
    render_header(
        "System Health",
        "Render deployment health, API status, database checks, and route inventory.",
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

if page == "Dashboard":
    render_dashboard_home()

elif page == "Players":
    render_players_page()

elif page == "Teams":
    render_teams_page()

elif page == "Games":
    render_games_page()

elif page == "Predictions":
    render_predictions_page()

elif page == "AI Assistant":
    render_ai_assistant_page()

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

st.caption(
    "AISP Baseball Analytics Engine | Phase 3.11 Enterprise Dashboard Platform"
)


# ============================================================
# SECTION 18 - FUTURE FRONTEND ROADMAP
# ============================================================

"""
Phase 3.12

Player cards
Team cards
Leaderboards
Statcast visuals
Prediction confidence meters
Charts
Filters

Phase 3.13

Streamlit Cloud or Render dashboard deployment

Phase 3.14

Dedicated React / Next.js frontend

Phase 4.00

Sportsbook Intelligence UI
"""