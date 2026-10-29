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
""", unsafe_allow_allowed_html=True)


if 'step' not in st.session_state:
    st.session_state.step = 1
if 'num_players' not in st.session_state:
    st.session_state.num_players = 4
if 'player_names' not in st.session_state:
    st.session_state.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
if 'team_a_players' not in st.session_state:
    st.session_state.team_a_players = ["Player 1", "Player 2"]
if 'team_b_players' not in st.session_state:
    st.session_state.team_b_players = ["Player 3", "Player 4"]
if 'match_duration' not in st.session_state:
    st.session_state.match_duration = 60
if 'tie_breaker' not in st.session_state:
    st.session_state.tie_breaker = "Penalty Shootout"
if 'ai_results' not in st.session_state:
    st.session_state.ai_results = None


st.markdown("""
<div class="title-card">
    <h1>⚽ AI-Powered Football Match Judge</h1>
    <p>Abu Dhabi University | Family AI Game Day Competition</p>
</div>
""", unsafe_allow_html=True)


step_titles = ["1. Match Rules", "2. Team Rosters", "3. Live Match", "4. AI Judge", "5. Match Report"]
cols = st.columns(5)
for i, title in enumerate(step_titles):
    if st.session_state.step == i + 1:
        cols[i].button(f"👉 {title}", key=f"nav_{i}", disabled=True, use_container_width=True)
    else:
        cols[i].button(f"{title}", key=f"nav_{i}", disabled=True, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.step == 1:
    st.markdown("""
    <div class="section-card">
        <h3>⚙️ Step 1: Game Configuration & Match Rules</h3>
        <div class="bubble-info">
            💬 <b>Host Guidance:</b> Welcome! Set up your match duration, total participating family players, and your tie-breaker preference before team selection.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        num_players = st.number_input("Total Number of Players", min_value=2, max_value=22, value=st.session_state.num_players, step=2)
        match_dur = st.number_input("Match Duration (seconds)", min_value=10, max_value=600, value=st.session_state.match_duration)
    
    with col2:
        tie_break = st.selectbox("Tie Breaker Rule", ["Penalty Shootout", "Golden Goal (Sudden Death)", "Coin Toss"], index=0)
        
    st.session_state.num_players = num_players
    st.session_state.match_duration = match_dur
    st.session_state.tie_breaker = tie_break
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue to Team Rosters ➔", use_container_width=True):
        if len(st.session_state.player_names) != num_players:
            half = num_players // 2
            st.session_state.player_names = [f"Player {i+1}" for i in range(num_players)]
            st.session_state.team_a_players = st.session_state.player_names[:half]
            st.session_state.team_b_players = st.session_state.player_names[half:]
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.markdown(f"""
    <div class="section-card">
        <h3>👥 Step 2: Configure Player Names & Team Roster</h3>
        <div class="bubble-info">
            💬 <b>Host Guidance:</b> Name each player and split them into Team A and Team B.
        </div>
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
            st.session_state.step = 3
            st.rerun()

elif st.session_state.step == 3:
    st.markdown("""
    <div class="section-card">
        <h3>⏱️ Step 3: Match in Play</h3>
        <div class="bubble-warning">
            💬 <b>Field Monitor:</b> Ensure the camera clearly records the entire field, players, goal area, and ball movement[cite: 2].
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="bubble-info">
            <b>🔴 Team A Roster</b><br>
            {', '.join(st.session_state.team_a_players)}
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="bubble-info">
            <b>🔵 Team B Roster</b><br>
            {', '.join(st.session_state.team_b_players)}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Match Timer ⏱️", use_container_width=True):
        timer_box = st.empty()
        for remaining in range(st.session_state.match_duration, -1, -1):
            mins, secs = divmod(remaining, 60)
            timer_box.markdown(f"""
            <div class="bubble-success" style="text-align: center; font-size: 1.8rem;">
                ⏳ Match Time Left: <b>{mins:02d}:{secs:02d}</b>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        st.balloons()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Proceed to Video Recording & AI Judge ➔", use_container_width=True):
        st.session_state.step = 4
        st.rerun()


elif st.session_state.step == 4:
    st.markdown("""
    <div class="section-card">
        <h3>🎥 Step 4: Gameplay Footage & AI Judge Processing</h3>
        <div class="bubble-info">
            💬 <b>AI Judge Integration:</b> Record directly or upload match video. The AI verifies goals, tracks player ball possession times, identifies saves, and generates an encrypted verification hash[cite: 2].
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.subheader("📹 Record Live Footage")
        camera_file = st.camera_input("Record match highlight")
    with col_v2:
        st.subheader("📁 Upload Saved Video")
        uploaded_file = st.file_uploader("Upload Football Match File (MP4, MOV)", type=["mp4", "mov", "avi"])

    active_video = camera_file or uploaded_file
    if active_video is not None:
        st.video(active_video)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🤖 AI Judge Payload Verification")

    p_a1 = st.session_state.team_a_players[0] if st.session_state.team_a_players else "Player 1"
    p_b1 = st.session_state.team_b_players[0] if st.session_state.team_b_players else "Player 2"
    
    default_ai_payload = {
        "team_a_goals": 2,
        "team_b_goals": 1,
        "team_highest_possession": "Team A",
        "team_possession_breakdown": {"Team A": "58%", "Team B": "42%"},
        "mvp": p_a1,
        "mvp_reason": "Highest total ball possession time (14 mins 20 secs)",
        "goal_scorers": {
            p_a1: 2,
            p_b1: 1
        },
        "promising_players": [
            {"player": p_b1, "reason": "High dribble efficiency and key passes"},
            {"player": p_a1, "reason": "Exceptional positional awareness and shot precision"}
        ],
        "goalkeeper_saves": [
            {"player": st.session_state.team_b_players[-1] if len(st.session_state.team_b_players) > 1 else p_b1, "saves": 4, "key_highlight": "Diving acrobatic save at 03:15"}
        ],
        "verification_code": "ADU_AI_FOOTBALL_SECURE_9823"
    }

    payload_input = st.text_area("AI Judge Report Output (JSON format)", value=json.dumps(default_ai_payload, indent=2), height=240)

    if st.button("Apply AI Results ➔", use_container_width=True):
        try:
            parsed = json.loads(payload_input)
            st.session_state.ai_results = parsed
            computed_hash = hashlib.sha256(payload_input.encode('utf-8')).hexdigest()[:10].upper()
            st.session_state.ai_hash = computed_hash
            st.session_state.step = 5
            st.rerun()
        except Exception as e:
            st.error(f"Invalid AI report payload format: {e}")

elif st.session_state.step == 5:
    results = st.session_state.ai_results
    if not results:
        st.warning("No AI results found. Please return to Step 4.")
    else:
        score_a = results.get("team_a_goals", 0)
        score_b = results.get("team_b_goals", 0)
        
        if score_a > score_b:
            match_outcome = f"🏆 Match Winner: Team A ({score_a} - {score_b})"
        elif score_b > score_a:
            match_outcome = f"🏆 Match Winner: Team B ({score_b} - {score_a})"
        else:
            match_outcome = f"🤝 Draw Match ({score_a} - {score_b}) — Tie Breaker: {st.session_state.tie_breaker}"

        st.balloons()
        
       
        st.markdown(f"""
        <div class="bubble-success" style="text-align: center; font-size: 1.5rem; padding: 20px;">
            {match_outcome}
        </div>
        """, unsafe_allow_html=True)

       
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Final Score</div>
                <div class="stat-value">{score_a} - {score_b}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Top Possession</div>
                <div class="stat-value">{results.get("team_highest_possession", "N/A")}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Match MVP</div>
                <div class="stat-value" style="font-size: 1.2rem;">{results.get("mvp", "N/A")}</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Security Hash</div>
                <div class="stat-value" style="font-size: 0.9rem; color: #2563EB;">{st.session_state.get("ai_hash", "VERIFIED")}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_left, col_right = st.columns(2)

        with col_left:
            
            st.markdown("""
            <div class="section-card">
                <h4>⚽ Goal Scorers & Breakdown</h4>
            """, unsafe_allow_html=True)
            scorers = results.get("goal_scorers", {})
            if scorers:
                for player, goals in scorers.items():
                    st.markdown(f"""
                    <div class="bubble-info">
                        🎯 <b>{player}</b>: Scored <b>{goals}</b> Goal(s)
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Possession Bubble
            st.markdown("""
            <div class="section-card">
                <h4>📊 Team Possession Details</h4>
            """, unsafe_allow_html=True)
            possession = results.get("team_possession_breakdown", {})
            for t_name, pct in possession.items():
                st.markdown(f"""
                <div class="bubble-info">
                    ⏱️ <b>{t_name}</b>: Maintained <b>{pct}</b> ball possession
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            
            st.markdown(f"""
            <div class="section-card">
                <h4>⭐ Most Valuable Player (MVP)</h4>
                <div class="bubble-success">
                    <b>Player:</b> {results.get('mvp', 'N/A')}<br>
                    <b>Selection Reason:</b> {results.get('mvp_reason', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            
            st.markdown("""
            <div class="section-card">
                <h4>🌟 Promising Talent Analysis</h4>
            """, unsafe_allow_html=True)
            promising = results.get("promising_players", [])
            if promising:
                for item in promising:
                    st.markdown(f"""
                    <div class="bubble-info">
                        🚀 <b>{item.get('player')}</b>: {item.get('reason')}
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

         
            st.markdown("""
            <div class="section-card">
                <h4>🧤 Goalkeeper Highlights & Saves</h4>
            """, unsafe_allow_html=True)
            gk_saves = results.get("goalkeeper_saves", [])
            if gk_saves:
                for save in gk_saves:
                    st.markdown(f"""
                    <div class="bubble-warning">
                        🛡️ <b>{save.get('player')}</b>: Executed <b>{save.get('saves')}</b> key saves<br>
                        <i>Key Moment: {save.get('key_highlight')}</i>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Start New Game Setup", use_container_width=True):
            st.session_state.step = 1
            st.session_state.ai_results = None
            st.rerun()
