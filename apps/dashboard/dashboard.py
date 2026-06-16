# SECTION 1: Imports
import requests
import streamlit as st


# SECTION 2: Dashboard Config
API_BASE = "http://127.0.0.1:8000"
st.set_page_config(page_title="AISP Baseball", layout="wide")
st.title("AISP Baseball Analytics Engine")


# SECTION 3: Player Search
query = st.text_input("Search MLB player", value="Juan Soto")
if st.button("Search"):
    response = requests.get(f"{API_BASE}/players/search", params={"q": query}, timeout=20)
    st.dataframe(response.json())


# SECTION 4: Chatbot
message = st.text_input("Ask the AISP chatbot", value="Predict Juan Soto hit probability")
if st.button("Ask AISP"):
    response = requests.post(f"{API_BASE}/chat", json={"message": message}, timeout=20)
    st.json(response.json())
