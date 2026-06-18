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
        "Enterprise baseball intelligence platform for MLB data, player research, predictions, and AI-assisted sports analysis.",
        [
            "MLB Intelligence",
            "Prediction Engine",
            "AI Analyst",
            "Warehouse",
            "Render Live",
        ],
    )

    health = api_get("/health", timeout=5)

    api_online = bool(health)
    database_online = bool(
        isinstance(health, dict)
        and health.get("database")
    )

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
            "SQLite warehouse status",
        )

    with c3:
        render_metric_card(
            "Sport",
            "MLB",
            "Baseball module active",
        )

    with c4:
        render_metric_card(
            "Platform",
            "Phase 4.00",
            "AI aesthetic layer",
        )

    st.divider()

    st.markdown("<div class='section-kicker'>Platform Modules</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Enterprise Sports Intelligence</div>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)

    with m1:
        render_glass_card(
            "Player Intelligence",
            "Search MLB players, inspect roster context, view profile fields, and prepare player-level predictions.",
        )

    with m2:
        render_glass_card(
            "Prediction Workbench",
            "Review prediction endpoints and prepare model outputs for hits, home runs, game winners, and props.",
        )

    with m3:
        render_glass_card(
            "AI Analyst",
            "Ask natural language baseball questions and route them through the database-aware AI chat system.",
        )

    st.divider()

    st.markdown("<div class='section-kicker'>Quick Actions</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>System Controls</div>", unsafe_allow_html=True)

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("Run Health Check", use_container_width=True):
            st.json(api_get("/health"))

    with q2:
        if st.button("View API Routes", use_container_width=True):
            st.json(api_get("/system/routes"))

    with q3:
        if st.button("System Info", use_container_width=True):
            st.json(api_get("/system/info"))


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
# SECTION 11 - PREDICTIONS PAGE
# ============================================================

def render_predictions_page() -> None:
    render_header(
        "Prediction Workbench",
        "Review prediction outputs, model confidence, player props, and future simulation engines.",
        ["Hit Probability", "Home Runs", "Game Winner", "Monte Carlo"],
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
        st.subheader("AI Prediction Lab")

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

        render_glass_card(
            "Coming Next",
            "This lab will become the control room for simulations, sportsbook-style projections, and AI explanations.",
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
        "Analytics Center",
        "Future command center for batting, pitching, fielding, Statcast, and leaderboard intelligence.",
        ["Batting", "Pitching", "Fielding", "Statcast"],
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card("Batting", "Planned", "Leaderboards and player cards")

    with col2:
        render_metric_card("Pitching", "Planned", "ERA, WHIP, K-rate, projections")

    with col3:
        render_metric_card("Fielding", "Planned", "Position and defensive metrics")

    with col4:
        render_metric_card("Statcast", "Planned", "Exit velocity, barrels, xwOBA")

    st.warning(
        "Phase 4.01 will add charts, player cards, comparison tables, and visual leaderboards."
    )


# ============================================================
# SECTION 14 - WAREHOUSE PAGE
# ============================================================

def render_warehouse_page() -> None:
    render_header(
        "Data Warehouse",
        "Monitor database health, sync readiness, table coverage, and future data quality scoring.",
        ["Teams", "Players", "Stats", "Games", "Predictions"],
    )

    info = api_get("/system/info")

    if info:
        st.json(info)

    st.divider()

    render_glass_card(
        "Warehouse Roadmap",
        "Upcoming: row counts, sync timestamps, table health, data quality scores, and nightly ingestion job status.",
    )


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