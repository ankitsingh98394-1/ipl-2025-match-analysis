import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="IPL 2025 Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished aesthetic
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 12px;
        border-left: 5px solid #3b82f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1rem;
        padding-top: 8px;
        padding-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Path resolution relative to this file
BASE_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
DATA = BASE_DIR / "data"

st.markdown('<div class="main-title">🏏 IPL 2025 Match Analysis & Insights</div>', unsafe_allow_html=True)
st.caption("College Data Science Project | Built with Python • Pandas • Plotly • Streamlit")

@st.cache_data
def load_csv(name):
    path = DATA / name
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Error loading {name}: {e}")
        return None

matches = load_csv("matches.csv")
batting = load_csv("orange_cap.csv")
bowling = load_csv("purple_cap.csv")

if matches is None:
    st.error("⚠️ `matches.csv` is missing. Place it inside the `data/` folder.")
    st.info("Check README.md for dataset requirements and format.")
    st.stop()

# Standardise columns
matches.columns = [c.strip().lower().replace(" ", "_") for c in matches.columns]

aliases = {
    "team1": ["team1", "team_1", "first_team"],
    "team2": ["team2", "team_2", "second_team"],
    "winner": ["winner", "winning_team", "match_winner"],
    "toss_winner": ["toss_winner", "tosswinner"],
    "toss_decision": ["toss_decision", "toss_decision_type"],
    "venue": ["venue", "stadium", "city"],
    "player_of_match": ["player_of_match", "player_of_the_match", "pom", "mom"],
    "date": ["date", "match_date"],
    "win_by": ["win_by", "won_by", "result_type"],
    "result_margin": ["result_margin", "margin", "win_margin"]
}

def find_col(df, choices):
    for c in choices:
        if c in df.columns:
            return c
    return None

winner_col = find_col(matches, aliases["winner"])
team1_col = find_col(matches, aliases["team1"])
team2_col = find_col(matches, aliases["team2"])
venue_col = find_col(matches, aliases["venue"])
toss_col = find_col(matches, aliases["toss_winner"])
toss_decision_col = find_col(matches, aliases["toss_decision"])
pom_col = find_col(matches, aliases["player_of_match"])
win_by_col = find_col(matches, aliases["win_by"])
margin_col = find_col(matches, aliases["result_margin"])

if winner_col is None:
    st.error("Could not find a valid winner column. Rename the winner column to 'winner'.")
    st.write("Available columns:", list(matches.columns))
    st.stop()

# Data Cleaning
matches = matches.copy()
matches[winner_col] = matches[winner_col].fillna("No Result")
matches = matches[~matches[winner_col].astype(str).str.lower().isin(["nan", "no result", "abandoned"])]

# Extract complete team roster
if team1_col and team2_col:
    all_teams = sorted(list(set(matches[team1_col].dropna().unique()).union(set(matches[team2_col].dropna().unique()))))
else:
    all_teams = sorted(set(matches[winner_col].dropna().astype(str)))

# Team Colors Palette for consistent branding
TEAM_COLORS = {
    "Chennai Super Kings": "#FACC15",
    "Mumbai Indians": "#004BA0",
    "Royal Challengers Bengaluru": "#DA1818",
    "Kolkata Knight Riders": "#3A225D",
    "Rajasthan Royals": "#EA1A85",
    "Sunrisers Hyderabad": "#F26522",
    "Delhi Capitals": "#0078BC",
    "Lucknow Super Giants": "#0057E7",
    "Gujarat Titans": "#1B2133",
    "Punjab Kings": "#DD1F2D"
}

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("⚙️ Dashboard Filters")
    filter_mode = st.radio("Team Filtering Mode:", ["Participating Teams", "Winning Team Only"], index=0)
    
    col_btn1, col_btn2 = st.columns(2)
    select_all = col_btn1.button("Select All")
    clear_all = col_btn2.button("Clear")
    
    if select_all:
        default_selection = all_teams
    elif clear_all:
        default_selection = []
    else:
        default_selection = all_teams

    selected_teams = st.multiselect(
        "Teams:", 
        options=all_teams, 
        default=default_selection
    )
    
    # Venue Filter
    if venue_col:
        all_venues = sorted(matches[venue_col].dropna().unique())
        selected_venues = st.multiselect("Venues (Optional):", options=all_venues, default=all_venues)
    else:
        selected_venues = []

if not selected_teams:
    st.warning("👈 Please select at least one team from the sidebar filters.")
    st.stop()

# Apply Filters
if filter_mode == "Winning Team Only":
    filtered = matches[matches[winner_col].astype(str).isin(selected_teams)]
else:
    if team1_col and team2_col:
        filtered = matches[
            matches[team1_col].astype(str).isin(selected_teams) | 
            matches[team2_col].astype(str).isin(selected_teams)
        ]
    else:
        filtered = matches[matches[winner_col].astype(str).isin(selected_teams)]

if venue_col and selected_venues:
    filtered = filtered[filtered[venue_col].isin(selected_venues)]

# ----------------- TOP METRICS -----------------
total_matches = len(matches)
filtered_matches_count = len(filtered)
leading_team = matches[winner_col].value_counts().idxmax() if total_matches else "N/A"
leading_team_wins = matches[winner_col].value_counts().max() if total_matches else 0

toss_matches = matches[toss_col].notna().sum() if toss_col else 0
toss_win_rate = (matches.loc[matches[toss_col] == matches[winner_col]].shape[0] / toss_matches * 100) if toss_matches else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Tournament Matches", total_matches, f"{filtered_matches_count} in view")
m2.metric("Total Teams", len(all_teams))
m3.metric("Table Leader", leading_team, f"{leading_team_wins} Wins")
m4.metric("Toss Win -> Match Win", f"{toss_win_rate:.1f}%", "Historical IPL Avg ~51%")

st.write("")

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Team Performance", 
    "🪙 Toss Dynamics", 
    "⭐ Star Players", 
    "👑 Leaderboards (Cap)", 
    "📋 Match Log"
])

# ----- TAB 1: TEAM PERFORMANCE -----
with tab1:
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Wins by Franchise")
        win_counts = filtered[winner_col].value_counts().rename_axis("Team").reset_index(name="Wins")
        
        # Color mapping
        bar_colors = [TEAM_COLORS.get(t, "#2563EB") for t in win_counts["Team"]]
        fig_wins = go.Figure(data=[
            go.Bar(
                x=win_counts["Team"],
                y=win_counts["Wins"],
                text=win_counts["Wins"],
                textposition='outside',
                marker_color=bar_colors
            )
        ])
        fig_wins.update_layout(
            title="Team-wise Match Wins",
            xaxis_title="Team",
            yaxis_title="Total Wins",
            xaxis_tickangle=-45,
            template="plotly_white",
            margin=dict(t=40, b=80)
        )
        st.plotly_chart(fig_wins, use_container_width=True)

    with col_right:
        st.subheader("Top Stadiums by Matches")
        if venue_col:
            venue_counts = filtered[venue_col].fillna("Unknown").value_counts().head(10).rename_axis("Venue").reset_index(name="Matches")
            fig_venues = px.bar(
                venue_counts,
                x="Matches",
                y="Venue",
                orientation="h",
                text="Matches",
                color="Matches",
                color_continuous_scale="Viridis",
                title="Top 10 Host Venues"
            )
            fig_venues.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                template="plotly_white",
                margin=dict(t=40)
            )
            st.plotly_chart(fig_venues, use_container_width=True)
        else:
            st.info("Venue column not available.")

    # Win Type Distribution (Runs vs Wickets)
    if win_by_col:
        st.subheader("Victory Method Distribution")
        win_by_counts = filtered[win_by_col].str.lower().value_counts().reset_index()
        win_by_counts.columns = ["Result Type", "Count"]
        fig_wb = px.pie(
            win_by_counts, 
            names="Result Type", 
            values="Count", 
            hole=0.45,
            color="Result Type",
            color_discrete_map={"wickets": "#3b82f6", "runs": "#f97316"}
        )
        fig_wb.update_layout(template="plotly_white")
        st.plotly_chart(fig_wb, use_container_width=True)

# ----- TAB 2: TOSS DYNAMICS -----
with tab2:
    col_toss1, col_toss2 = st.columns(2)
    with col_toss1:
        st.subheader("Toss Winner Match Outcome")
        if toss_col:
            toss_data = matches.dropna(subset=[toss_col, winner_col]).copy()
            toss_data["Toss Winner Won Match"] = toss_data[toss_col] == toss_data[winner_col]
            outcome_df = toss_data["Toss Winner Won Match"].value_counts().reset_index()
            outcome_df.columns = ["Outcome", "Matches"]
            outcome_df["Outcome"] = outcome_df["Outcome"].map({True: "Won Match", False: "Lost Match"})
            
            fig_pie_toss = px.pie(
                outcome_df,
                names="Outcome",
                values="Matches",
                hole=0.4,
                color="Outcome",
                color_discrete_map={"Won Match": "#10B981", "Lost Match": "#EF4444"},
                title="Did the Toss Winner Win the Match?"
            )
            fig_pie_toss.update_layout(template="plotly_white")
            st.plotly_chart(fig_pie_toss, use_container_width=True)
        else:
            st.info("Toss winner column not found.")

    with col_toss2:
        st.subheader("Toss Decision Preference")
        if toss_decision_col:
            dec_counts = matches[toss_decision_col].str.capitalize().value_counts().reset_index()
            dec_counts.columns = ["Decision", "Count"]
            fig_dec = px.bar(
                dec_counts,
                x="Decision",
                y="Count",
                color="Decision",
                text="Count",
                color_discrete_map={"Field": "#0284C7", "Bat": "#F59E0B"},
                title="Captains' Decision After Winning Toss"
            )
            fig_dec.update_layout(template="plotly_white")
            st.plotly_chart(fig_dec, use_container_width=True)
        else:
            st.info("Toss decision column not found.")

# ----- TAB 3: STAR PLAYERS -----
with tab3:
    st.subheader("Most Player of the Match Awards")
    if pom_col:
        pom_counts = filtered[pom_col].fillna("Unknown").value_counts().head(12).rename_axis("Player").reset_index(name="Awards")
        fig_pom = px.bar(
            pom_counts,
            x="Awards",
            y="Player",
            orientation="h",
            color="Awards",
            text="Awards",
            color_continuous_scale="Purples",
            title="Top 12 Match Winners (POM Awards)"
        )
        fig_pom.update_layout(yaxis={'categoryorder': 'total ascending'}, template="plotly_white")
        st.plotly_chart(fig_pom, use_container_width=True)
    else:
        st.info("Player of the match column not found.")

# ----- TAB 4: LEADERBOARDS -----
with tab4:
    col_lead1, col_lead2 = st.columns(2)
    with col_lead1:
        st.subheader("🟠 Orange Cap (Leading Run Scorers)")
        if batting is not None:
            bat_df = batting.copy()
            bat_df.columns = [c.strip().title().replace("_", " ") for c in bat_df.columns]
            st.dataframe(bat_df, use_container_width=True, hide_index=True)
        else:
            st.info("Place `orange_cap.csv` in `data/` to view batting leaderboard.")

    with col_lead2:
        st.subheader("🟣 Purple Cap (Leading Wicket Takers)")
        if bowling is not None:
            bowl_df = bowling.copy()
            bowl_df.columns = [c.strip().title().replace("_", " ") for c in bowl_df.columns]
            st.dataframe(bowl_df, use_container_width=True, hide_index=True)
        else:
            st.info("Place `purple_cap.csv` in `data/` to view bowling leaderboard.")

# ----- TAB 5: MATCH LOG -----
with tab5:
    st.subheader("Complete Match Records")
    st.write(f"Showing **{len(filtered)}** matches matching the current sidebar filters.")
    
    # Download button for filtered dataset
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Matches CSV",
        data=csv_data,
        file_name="ipl_2025_filtered_matches.csv",
        mime="text/csv"
    )
    st.dataframe(filtered, use_container_width=True)

st.markdown("---")
st.caption("IPL 2025 Project Dashboard • Powered by Streamlit & Plotly")
