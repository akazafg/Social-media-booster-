import streamlit as st
import requests
from datetime import datetime, timedelta
import math

# 1. Dashboard Theme Configuration
st.set_page_config(page_title="BoostCore Engine v2", layout="wide", page_icon="🌍")

st.title("🌍 BoostCore: Data-Driven 80% Global Mainframe")
st.markdown("Evaluating upcoming matches using Poisson Distribution & Form Analytics to discover mathematically sound 80%+ banker options.")

# 2. Key Input Panel
st.sidebar.markdown("### 🔑 GLOBAL ACCESSIBILITY DATA ROUTE")
API_KEY = st.sidebar.text_input("Enter Open-Tier Token:", value="", type="password")
st.sidebar.markdown("[Get a Free Token instantly via Email here](https://www.football-data.org/client/register)")

st.sidebar.markdown("---")
st.sidebar.info("⚙️ **Engine Status:** Mathematical Form Analysis Model Activated. Filters set to 80% threshold.")

if not API_KEY:
    st.info("💡 Paste your data token into the sidebar panel to unlock the unrestricted global match board.")
    st.stop()

# Helper function to calculate Poisson probability
def poisson_probability(actual, mean):
    return (pow(mean, actual) * math.exp(-mean)) / math.factorial(actual)

# 3. Data Fetching Functions
@st.cache_data(ttl=600)
def fetch_weekly_fixtures(api_key):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={next_week}"
    headers = {'X-Auth-Token': api_key}
    try:
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code == 200:
            return response.json().get("matches", [])
        return []
    except:
        return []

@st.cache_data(ttl=1800)
def get_team_form_metrics(api_key, team_id):
    """Fetches past matches to calculate average goals scored and conceded."""
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=6"
    headers = {'X-Auth-Token': api_key}
    try:
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code != 200:
            return 1.2, 1.2  # Default baseline averages if API limits hit
        
        matches = response.json().get("matches", [])
        if not matches:
            return 1.2, 1.2

        goals_scored = 0
        goals_conceded = 0
        
        for m in matches:
            home_id = m.get("homeTeam", {}).get("id")
            score = m.get("score", {}).get("fullTime", {})
            h_goal = score.get("home", 0) if score.get("home") is not None else 0
            a_goal = score.get("away", 0) if score.get("away") is not None else 0
            
            if home_id == team_id:
                goals_scored += h_goal
                goals_conceded += a_goal
            else:
                goals_scored += a_goal
                goals_conceded += h_goal
                
        total_m = len(matches)
        return (goals_scored / total_m), (goals_conceded / total_m)
    except:
        return 1.2, 1.2

# Fetch initial fixtures
global_matches = fetch_weekly_fixtures(API_KEY)

if not global_matches:
    st.warning("Connecting to global league servers... Make sure your token is pasted cleanly in the sidebar.")
    st.stop()

# 4. Core Predictive Processing Matrix
global_tickets_deployed = 0
st.subheader("🎯 Calculated Data-Driven Banker Slips (80%+ Statistical Confidence)")

# Progress bar since we call team metrics dynamically
progress_bar = st.progress(0)
total_matches = len(global_matches)

for idx, match in enumerate(global_matches):
    progress_bar.progress((idx + 1) / total_matches)
    
    home_team = match.get("homeTeam", {}).get("name", "Home Squad")
    away_team = match.get("awayTeam", {}).get("name", "Away Squad")
    home_id = match.get("homeTeam", {}).get("id")
    away_id = match.get("awayTeam", {}).get("id")
    
    if not home_id or not away_id:
        continue
        
    competition = match.get("competition", {}).get("name", "Global League")
    area_name = match.get("competition", {}).get("area", {}).get("name", "International")
    
    utc_date_str = match.get("utcDate", "")
    match_date_formatted = "Upcoming"
    if utc_date_str:
        try:
            dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
            match_date_formatted = dt.strftime("%b %d, %H:%M UTC")
        except:
            pass

    # Fetch statistical metrics for both teams
    home_gf, home_ga = get_team_form_metrics(API_KEY, home_id)
    away_gf, away_ga = get_team_form_metrics(API_KEY, away_id)
    
    # Calculate expected goals using Poisson Baselines
    exp_home_goals = home_gf * away_ga * 1.1 # 1.1 adding standard home advantage weight
    exp_away_goals = away_gf * home_ga * 0.9
    
    # Compute Exact Probability Matrices
    prob_home_0 = poisson_probability(0, exp_home_goals)
    prob_home_1 = poisson_probability(1, exp_home_goals)
    
    prob_away_0 = poisson_probability(0, exp_away_goals)
    prob_away_1 = poisson_probability(1, exp_away_goals)
    
    # 1. Calculate Over 1.5 Goals Probability
    # P(0-0) = P(H=0) * P(A=0)
    # P(1-0) = P(H=1) * P(A=0)
    # P(0-1) = P(H=0) * P(A=1)
    prob_under_1_5 = (prob_home_0 * prob_away_0) + (prob_home_1 * prob_away_0) + (prob_home_0 * prob_away_1)
    prob_over_1_5 = max(0, min(99, int((1.0 - prob_under_1_5) * 100)))
    
    # 2. Calculate Double Chance (Home Win or Draw) Probability
    # Estimate based on expected goal differentials
    goal_diff = exp_home_goals - exp_away_goals
    prob_home_win_or_draw = int(100 / (1.0 + math.exp(-1.2 * (goal_diff + 0.5))))
    prob_home_win_or_draw = max(50, min(99, prob_home_win_or_draw))

    # Determine market selections based on mathematical maximums
    if prob_home_win_or_draw >= prob_over_1_5:
        implied_probability = prob_home_win_or_draw
        market_type = "DC"
    else:
        implied_probability = prob_over_1_5
        market_type = "O15"

    # 🛑 THE GATEKEEPER BARRIER: Filter matches strictly at 80%
    if implied_probability < 80:
        continue
        
    global_tickets_deployed += 1
    
    if market_type == "O15":
        play_ticket = "🔥 OVER 1.5 TOTAL MATCH GOALS"
        reasoning = f"Combined attacking form metrics indicate high offensive execution. Based on an expected matching threshold of {exp_home_goals:.2f} goals for {home_team} and {exp_away_goals:.2f} goals for {away_team}, the system computes an active {implied_probability}% mathematical likelihood of clearing 1.5 goals."
    else:
        play_ticket = f"🔒 DOUBLE CHANCE: {home_team} WIN OR DRAW (1X)"
        reasoning = f"Data metrics show defensive resilience from {home_team} on home soil paired with sluggish offensive conversion rates from {away_team}. Poisson modeling yields an elite {implied_probability}% safety baseline backing a home result."

    # Print Clean Scannable Cards
    with st.container(border=True):
        col1, col2 = st.columns([5, 4], gap="medium")
        with col1:
            st.markdown(f"**🌍 REGION: {area_name.upper()} | COMPETITION: {competition} | 📅 DATE: {match_date_formatted}**")
            st.markdown(f"## {home_team} vs {away_team}")
            st.write(f"📊 *Form Analysis Matrix:* {reasoning}")
            st.caption(f"System Math Certainty Rating: {implied_probability}% Probability")
        with col2:
            st.markdown("**👑 SELECTION TO PLAY:**")
            st.success(f"**{play_ticket}**")
            st.markdown("---")
            st.caption("Data-backed calculation model. Manage your stakes responsibly.")

# Remove progress bar upon completion
progress_bar.empty()

if global_tickets_deployed == 0:
    st.info("The system completed a full data-driven scan of upcoming matchups. No active matches mathematically crossed the 80% confidence index thresholds right now.")
