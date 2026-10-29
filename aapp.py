import streamlit as st
import time
import hashlib
import json

st.set_page_config(
    page_title="FAMILY AI GAME DAY", 
    layout="wide", 
    page_icon="⚽"
)


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


st.markdown("""
<div class="title-card">
    <h1>⚽ FAMILY AI GAME DAY</h1>
    <p>Abu Dhabi University | Family AI Game Day Competition</p>
</div>
""", unsafe_allow_html=True)

step_titles = ["1. Choose Game", "2. Match Rules", "3. Team Rosters", "4. Live Match", "5. AI Judge", "6. Match Report"]
cols = st.columns(6)
for i, title in enumerate(step_titles):
    if st.session_state.step == i + 1:
        cols[i].button(f"👉 {title}", key=f"nav_{i}", disabled=True, use_container_width=True)
    else:
        cols[i].button(f"{title}", key=f"nav_{i}", disabled=True, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


elif st.session_state.step == 3:
    st.markdown(f"""
    <div class="section-card">
        <h3>👥 Step 3: Configure Player Names & Team Roster</h3>
        <div class="bubble-info">
            💬 <b>Host Guidance:</b> Name each player and split them into Team A and Team B[cite: 1].
        </div>
        <span class="badge badge-primary">Game: {st.session_state.selected_game}</span>
        <span class="badge badge-primary">Total Players: {st.session_state.num_players}</span>
        <span class="badge badge-success">Match Time: {st.session_state.match_duration}s</span>
        <span class="badge badge-gold">Tie Breaker: {st.session_state.tie_breaker}</span>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📝 Player Names")
    updated_names = []
    p_cols = st.columns(2)
    for i in range(st.session_state.num_players):
        col_idx = 0 if i < st.session_state.num_players // 2 else 1
        with p_cols[col_idx]:
            default_val = st.session_state.player_names[i] if i < len(st.session_state.player_names) else f"Player {i+1}"
            p_name = st.text_input(f"Player {i+1} Name", value=default_val, key=f"pname_{i}")
            updated_names.append(p_name)
            
    st.session_state.player_names = updated_names

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🛡️ Team Assignment")
    col_ta, col_tb = st.columns(2)
    with col_ta:
        team_a = st.multiselect("Team A Players", options=updated_names, default=updated_names[:st.session_state.num_players // 2])
    with col_tb:
        team_b = st.multiselect("Team B Players", options=updated_names, default=[p for p in updated_names if p not in team_a])

    if st.button("Save Rosters & Proceed ➔", use_container_width=True):
        if not team_a or not team_b:
            st.error("Each team must have at least one player.")
        else:
            st.session_state.team_a_players = team_a
            st.session_state.team_b_players = team_b
            st.session_state.step = 4
            st.rerun()
    game_choices = {
        "⚽ Football": "Mandatory sports game. AI tracks goal scorers, ball possession time, saves, and MVP[cite: 2].",
        f"🎯 Game Idea 1: {st.session_state.game_idea_1_title}": "Original Game Idea 1. Target and precision tracking with AI scoring.",
        f"🐪 Game Idea 2: {st.session_state.game_idea_2_title}": "Original Game Idea 2. Heritage agility and body pose rhythm tracking."
    }

    selected = st.radio("Select Active Game:", list(game_choices.keys()), index=0)

    st.markdown(f"""
    <div class="bubble-success">
        <b>Selected Game Overview:</b> {game_choices[selected]}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Confirm Game Selection ➔", use_container_width=True):
        st.session_state.selected_game = selected
        st.session_state.step = 2
        st.rerun()


elif st.session_state.step == 2:
    st.markdown(f"""
    <div class="section-card">
        <h3>⚙️ Step 2: Game Configuration & Match Rules</h3>
        <div class="bubble-info">
            💬 <b>Host Guidance:</b> Set up your match duration, total participating players, custom scoring rules, and tie-breaker preferences[cite: 1].
        </div>
        <span class="badge badge-primary">Active Game: {st.session_state.selected_game}</span>
    </div>
    """, unsafe_allow_html=True)

    if "Football" in st.session_state.selected_game:
        default_rules = "1 Point per goal scored into target net. Goalkeeper saves prevent goals."
    elif "Game Idea 1" in st.session_state.selected_game:
        default_rules = "Bullseye = 10 pts, Middle Ring = 5 pts, Outer Ring = 2 pts."
    else:
        default_rules = "1 Point per rhythm cycle completed without stepping out of boundary."

    col1, col2 = st.columns(2)
    with col1:
        num_players = st.number_input("Total Number of Players", min_value=2, max_value=22, value=st.session_state.num_players, step=2)
        match_dur = st.number_input("Match Duration (seconds)", min_value=10, max_value=600, value=st.session_state.match_duration)
    
    with col2:
        tie_break = st.selectbox("Tie Breaker Rule", ["Penalty Shootout", "Golden Goal (Sudden Death)", "Coin Toss"], index=0)
        p_rules = st.text_area("Custom Game Rules", value=default_rules, height=80)
        
    st.session_state.num_players = num_players
    st.session_state.match_duration = match_dur
    st.session_state.tie_breaker = tie_break
    st.session_state.points_rules = p_rules
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue to Team Rosters ➔", use_container_width=True):
        if len(st.session_state.player_names) != num_players:
            half = num_players // 2
            st.session_state.player_names = [f"Player {i+1}" for i in range(num_players)]
            st.session_state.team_a_players = st.session_state.player_names[:half]
            st.session_state.team_b_players = st.session_state.player_names[half:]
        st.session_state.step = 3
        st.rerun()


elif st.session_state.step == 3:
    st.markdown(f"""
    <div class="section-card">
        <h3>👥 Step 3: Configure Player Names & Team Roster</h3>
        <div class="bubble-info">
            💬 <b>Host Guidance:</b> Name each player and split them into Team A and Team B[cite: 1].
        </div>
        <span class="badge badge-primary">Game: {st.session_state.selected_game}</span>
        <span class="badge badge-primary">Total Players: {st.session_state.num_players}</span>
        <span class="badge badge-success">Match Time: {st.session_state.match_duration}s</span>
        <span class="badge badge-gold">Tie Breaker: {st.session_state.tie_breaker}</span>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📝 Player Names")
    updated_names = []
    p_cols = st.columns(2)
    for i in range(st.session_state.num_players):
        col_idx = 0 if i < st.session_state.num_players // 2 else 1
        with p_cols[col_idx]:
            default_val = st.session_state.player_names[i] if i < len(st.session_state.player_names) else f"Player {i+1}"
            p_name = st.text_input(f"Player {i+1} Name", value=default_val, key=f"pname_{i}")
            updated_names.append(p_name)
            
    st.session_state.player_names = updated_names

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🛡️ Team Assignment")
    col_ta, col_tb = st.columns(2)
    with col_ta:
        team_a = st.multiselect("Team A Players", options=updated_names, default=updated_names[:st.session_state.num_players // 2])
    with col_tb:
        team_b = st.multiselect("Team B Players", options=updated_names, default=[p for p in updated_names if p not in team_a])

  if st.button("Save Rosters & Proceed ➔", use_container_width=True):
        if not team_a or not team_b:
            st.error("Each team must have at least one player.")
        else:
            st.session_state.team_a_players = team_a
            st.session_state.team_b_players = team_b
            st.session_state.step = 4
            st.rerun()
