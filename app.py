import streamlit as st
from supabase import create_client, Client
import urllib.request
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Social Media Booster", layout="wide", page_icon="🔥")

# 2. Database & Auth Connection
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("DATABASE ERROR: Missing core API secrets in Streamlit Cloud Settings panel.")
    st.stop()

if "user" not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION & LANDING MAINBOARD ---
if st.session_state.user is None:
    with st.sidebar:
        st.markdown("### ⚡ ENGINE STATUS")
        st.success("🌐 SERVER: ONLINE")
        st.markdown("---")
        st.markdown("### 🚀 PREMIUM EXTENSION")
        st.info("🌟 **LAUNCHING SEPT 2026**\n\nUnlock Tier-1 algorithms, neural image matrices, and bulk multi-platform pipelines.")

    # High-Converting Hero Header
    st.title("🔥 Social Media Booster Mainframe")
    st.subheader("START EARNING ON YOUR OWN SCHEDULE")
    st.markdown("⚡ *Free forever • No credit card required • Live instantly*")
    st.markdown("---")

    # Slushy Style Bold Metrics Grid
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="ACTIVE USERS", value="1,200+")
    with m_col2:
        st.metric(label="AVG. ENGAGEMENT BOOST", value="+410%")
    with m_col3:
        st.metric(label="COST TO RUN", value="$0 / MTH")

    st.markdown("---")
    st.markdown("#### 🔒 Access the Elite Content Optimization Mainframe")
    
    auth_tab1, auth_tab2 = st.tabs(["🔑 ACCESS ACCOUNT", "📝 INITIALIZE FREE PROFILE"])

    with auth_tab1:
        login_email = st.text_input("EMAIL ADDRESS", key="login_email_input")
        login_password = st.text_input("PASSWORD", type="password", key="login_pwd_input")
        if st.button("AUTHORIZE CONNECTION ➔", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error("ACCESS DENIED: Invalid credentials.")

    with auth_tab2:
        signup_email = st.text_input("REGISTER EMAIL", key="signup_email_input")
        signup_password = st.text_input("CREATE PASSWORD (6+ Chars)", type="password", key="signup_pwd_input")
        if st.button("INITIALIZE FREE ACCOUNT ➔", use_container_width=True):
            try:
                res = supabase.auth.sign_up({"email": signup_email, "password": signup_password})
                st.success("✅ Mainframe profile generated! Switch to the Access Account tab to log in.")
            except Exception as e:
                st.error(f"Registration Failed: {e}")

    st.stop()

# --- MAIN ENGINE INTERFACE (Runs if logged in) ---
with st.sidebar:
    st.markdown(f"👤 **OPERATOR:**\n`{st.session_state.user.email}`")
    st.markdown("---")
    st.markdown("### 🚀 PREMIUM TIERS")
    st.info("🌟 **RELEASING IN 2 MONTHS**\n\nPrepare for heavy-duty volume metrics and raw network amplification protocols.")
    st.markdown("---")
    if st.button("🚪 TERMINATE SESSION", use_container_width=True):
        supabase.auth.auth.sign_out()
        st.session_state.user = None
        st.rerun()

st.title("🔥 Social Media Booster Engine")
st.markdown("Convert raw thoughts and conceptual fragments into structural, high-performing text output.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 RAW INGESTION CORE")
    raw_text = st.text_area(
        "Input unoptimized post concept:",
        height=200,
        placeholder="Type raw draft, baseline statistics, or core context here..."
    )
    
    tone_style = st.selectbox(
        "Select Algorithmic Persona:",
        ["Thought Leader (Analytical & Bold)", "Storyteller (Emotional & Hooks)", "The Growth Hacker (Punchy & Short)"]
    )
    
    boost_trigger = st.button("🚀 EXECUTE CONTENT AMPLIFICATION", use_container_width=True)

with col2:
    st.markdown("### 📤 HIGH-PERFORMANCE OUTPUT")
    
    if "boosted_text" not in st.session_state:
        st.session_state.boosted_text = ""

    if boost_trigger:
        if not raw_text.strip():
            st.warning("Mainframe alert: Ingestion chamber is empty.")
        else:
            with st.spinner("Processing optimization matrices..."):
                try:
                    prompt = f"Optimize this text: '{raw_text}' using the '{tone_style}' framework for LinkedIn and X. Be an elite growth marketer."
                    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                    
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        boosted_content = response.read().decode('utf-8')
                    
                    st.session_state.boosted_text = boosted_content
                    
                    db_data = {
                        "user_input": raw_text,
                        "ai_output": boosted_content,
                        "platform": tone_style
                    }
                    supabase.table("generated_posts").insert(db_data).execute()
                    
                except Exception as e:
                    st.error(f"Execution Halt: {e}")

    if st.session_state.boosted_text:
        st.success("AMPLIFICATION MATRIX COMPLETE")
        st.markdown(st.session_state.boosted_text)
        st.markdown("---")
        st.text_area("📋 MAIN DATA STREAM (TAP TO COPY):", value=st.session_state.boosted_text, height=150)
