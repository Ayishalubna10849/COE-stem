import streamlit as st
import time
import hashlib
import json

st.set_page_config(
    page_title="FAMILY AI GAME DAY", 
    layout="wide", 
    page_icon="⚽"
)

# Custom Theme & Styling (Bubbles, Cards, Badges)
st.markdown("""
<style>
    /* Main Theme & Colors */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Title Banner */
    .title-card {
        background: linear-gradient(135deg, #1E3C72 0%, #2A5298 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .title-card h1 {
        color: #FFFFFF !important;
        margin-bottom: 0px;
        font-weight: 700;
    }
    .title-card p {
        color: #E0E6ED;
        margin-top: 5px;
        font-size: 1.1rem;
    }

    /* Section Containers */
    .section-card {
        background: #FFFFFF;
        padding: 22px;
        border-radius: 14px;
        border-left: 6px solid #2A5298;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Text & Chat Bubbles */
    .bubble-info {
        background-color: #EBF3FE;
        border: 1px solid #C2DAFE;
        border-radius: 18px 18px 18px 2px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #1E3C72;
        font-size: 1rem;
    }
    
    .bubble-success {
        background-color: #E6F4EA;
        border: 1px solid #B7E1CD;
        border-radius: 18px 18px 18px 2px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #137333;
        font-weight: 500;
    }

    .bubble-warning {
        background-color: #FEF7E0;
        border: 1px solid #FCE8E6;
        border-radius: 18px 18px 18px 2px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #B06000;
    }

    /* Stats Metric Cards */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stat-title {
        color: #64748B;
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .stat-value {
        color: #0F172A;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Custom Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-primary { background-color: #DBEAFE; color: #1E40AF; }
    .badge-success { background-color: #DCFCE7; color: #166534; }
    .badge-gold { background-color: #FEF3C7; color: #92400E; }
</style>
""", unsafe_allow_html=True)

# Session State Initializations
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = "Football"
if 'game_idea_1_title' not in st.session_state:
    st.session_state.game_idea_1_title = "Bedouin Oasis Archery & Dart Toss"
if 'game_idea_2_title' not in st.session_state:
    st.session_state.game_idea_2_title = "Camel Racing Rhythm & Agility Sprint"
if 'num_players' not in st.session_state:
    st.session_state.num_players = 4
if 'player_names' not in st.session_state:
    st.session_state.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
if 'team_a_players' not in st.session_state:
    st.session_state.team_a_players = ["Player 1", "Player 2"]
if 'team_b_players' not in st.session_state:
    st.session_state.team_b_players = ["Player 3", "Player 4"]
if 'points_rules' not in st.session_state:
    st.session_state.points_rules = "Standard score points per successful play."
if 'match_duration' not in st.session_state:
    st.session_state.match_duration = 60
if 'tie_breaker' not in st.session_state:
    st.session_state.tie_breaker = "Penalty Shootout"
if 'ai_results' not in st.session_state:
    st.session_state.ai_results = None

# Title Banner Card
st.markdown("""
<div class="title-card">
    <h1>⚽ FAMILY AI GAME DAY</h1>
    <p>Abu Dhabi University | Family AI Game Day Competition</p>
</div>
""", unsafe_allow_html=True)

# Navigation Bar
step_titles = ["1. Choose Game", "2. Match Rules", "3. Team Rosters", "4. Live Match", "5. AI Judge", "6. Match Report"]
cols = st.columns(6)
for i, title in enumerate(step_titles):
    if st.session_state.step == i + 1:
        cols[i].button(f"👉 {title}", key=f"nav_{i}", disabled=True, use_container_width=True)
    else:
        cols[i].button(f"{title}", key=f"nav_{i}", disabled=True, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# STEP 1: CHOOSE A GAME
# ==============================================================================
if st.session_state.step == 1:
    st.markdown("""
    <div class="section-card">
        <h3>🎮 Step 1: Specify & Select Your Family Game</h3>
        <div class="bubble-info">
            💬 <b>Host Guidance:</b> Select a game to play! Choose Football or customize your own 2 unique original games[cite: 1].
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        custom_g1 = st.text_input("Title for Game Idea 1", value=st.session_state.game_idea_1_title)
        st.session_state.game_idea_1_title = custom_g1
    with col_g2:
        custom_g2 = st.text_input("Title for Game Idea 2", value=st.session_state.game_idea_2_title)
