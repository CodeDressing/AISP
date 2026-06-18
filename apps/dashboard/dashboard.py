# ============================================================
# AISP BASEBALL ANALYTICS ENGINE
# PHASE 3.10 PART 1
# ENTERPRISE ANALYTICS DASHBOARD
# FILE: apps/dashboard/dashboard.py
# PURPOSE: primary user interface for MLB analytics,
# predictions, AI chat, and future sportsbook intelligence
# ============================================================

# ============================================================
# SECTION 01 - IMPORTS
# ============================================================

import requests
import streamlit as st


# ============================================================
# SECTION 02 - CONFIGURATION
# ============================================================

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AISP Baseball Analytics",
    page_icon="⚾",
    layout="wide",
)

# ============================================================
# SECTION 03 - CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
    }

    .aisp-header {
        font-size: 42px;
        font-weight: 800;
        color: white;
    }

    .aisp-subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 20px;
    }

    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SECTION 04 - HEADER
# ============================================================

st.markdown(
    """
    <div class="aisp-header">
        ⚾ AISP Baseball Analytics Engine
    </div>

    <div class="aisp-subtitle">
        Artificial Intelligence Sports Predictions
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SECTION 05 - SYSTEM STATUS
# ============================================================

st.subheader("System Status")

col1, col2, col3, col4 = st.columns(4)

try:
    health = requests.get(
        f"{API_BASE}/health",
        timeout=5,
    ).json()

    api_status = "ONLINE"

except Exception:
    api_status = "OFFLINE"

with col1:
    st.metric(
        "API",
        api_status,
    )

with col2:
    st.metric(
        "Sport",
        "MLB",
    )

with col3:
    st.metric(
        "Prediction Engine",
        "ACTIVE",
    )

with col4:
    st.metric(
        "AI Chat",
        "ACTIVE",
    )

# ============================================================
# SECTION 06 - MAIN LAYOUT
# ============================================================

left_column, right_column = st.columns(
    [2, 1]
)

# ============================================================
# SECTION 07 - PLAYER SEARCH CENTER
# ============================================================

with left_column:

    st.subheader(
        "Player Search"
    )

    player_query = st.text_input(
        "Search MLB Player",
        value="Juan Soto",
    )

    if st.button(
        "Search Player"
    ):

        try:

            response = requests.get(
                f"{API_BASE}/players/search",
                params={
                    "q": player_query,
                },
                timeout=20,
            )

            st.dataframe(
                response.json(),
                use_container_width=True,
            )

        except Exception as exc:

            st.error(
                f"Search failed: {exc}"
            )

# ============================================================
# SECTION 08 - AI CHAT PANEL
# ============================================================

with right_column:

    st.subheader(
        "AISP AI Assistant"
    )

    message = st.text_area(
        "Ask AISP",
        value="Predict Juan Soto hit probability",
        height=150,
    )

    if st.button(
        "Ask AI"
    ):

        try:

            response = requests.post(
                f"{API_BASE}/chat",
                json={
                    "message": message,
                },
                timeout=30,
            )

            st.json(
                response.json()
            )

        except Exception as exc:

            st.error(
                f"Chat failed: {exc}"
            )

# ============================================================
# SECTION 09 - TEAM ANALYTICS
# ============================================================

st.divider()

st.subheader(
    "MLB Team Analytics"
)

team_id = st.number_input(
    "Team ID",
    value=147,
)

if st.button(
    "Load Team"
):

    try:

        response = requests.get(
            f"{API_BASE}/teams/{team_id}",
            timeout=20,
        )

        st.json(
            response.json()
        )

    except Exception as exc:

        st.error(
            str(exc)
        )

# ============================================================
# SECTION 10 - PREDICTION WORKSPACE
# ============================================================

st.divider()

st.subheader(
    "Prediction Workspace"
)

prediction_type = st.selectbox(
    "Prediction Type",
    [
        "Hit Probability",
        "Home Run Probability",
        "Game Winner",
        "Strikeout Probability",
    ],
)

st.info(
    f"Selected Model: {prediction_type}"
)

# ============================================================
# SECTION 11 - FUTURE SPORTSBOOK PANEL
# ============================================================

st.divider()

st.subheader(
    "Sportsbook Intelligence"
)

st.warning(
    "Coming in Phase 4"
)

# ============================================================
# SECTION 12 - FOOTER
# ============================================================

st.divider()

st.caption(
    "AISP Baseball Analytics Engine | Enterprise MLB Intelligence Platform"
)