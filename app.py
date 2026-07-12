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
    st.error("DATABASE ERROR: Missing core API secrets.")
    st.stop()

# Track which form to show: "login" or "signup"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION PORTAL ---
if st.session_state.user is None:
    with st.sidebar:
        st.markdown("### ⚡ ENGINE STATUS")
        st.success("🌐 SERVER: ONLINE")
        st.markdown("---")
        st.markdown("### 🚀 PREMIUM EXTENSION")
        st.info("🌟 **LAUNCHING SEPT 2026**\n\nUnlock Tier-1 algorithms, advanced multi-platform variations, and automated content scheduling pipelines.")

    # Main Hero Presentation
    st.title("🔥 Social Media Booster Mainframe")
    st.markdown("⚡ *Transform raw text fragments into high-impact, formatted social media posts instantly.*")
    st.markdown("---")

    # High-Performance Metrics Grid
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="POSTS GENERATED", value="15,000+")
    with m_col2:
        st.metric(label="PROCESSING SPEED", value="< 2.5s")
    with m_col3:
        st.metric(label="AI EFFICIENCY", value="99.4%")

    st.markdown("---")

    # Dynamic Form Container matching SerpClix style
    if st.session_state.auth_mode == "login":
        st.markdown("### 🔑 Log in to your account")
        
        login_email = st.text_input("Email or Username*", key="login_email")
        login_password = st.text_input("Password*", type="password", key="login_pwd")
        
        if st.button("Log In", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error("ACCESS DENIED: Please verify your credentials or email activation state.")
        
        st.markdown("---")
        if st.button("Not registered? Create an account", key="go_to_signup"):
            st.session_state.auth_mode = "signup"
            st.rerun()

    else:
        st.markdown("### 📝 Create your account")
        
        signup_email = st.text_input("Email Address*", key="signup_email")
        signup_password = st.text_input("Password* (6+ characters)", type="password", key="signup_pwd")
        
        if st.button("Register Account", use_container_width=True):
            try:
                res = supabase.auth.sign_up({"email": signup_email, "password": signup_password})
                st.success("📩 VERIFICATION EMAIL SENT! Check your inbox to activate your profile.")
            except Exception as e:
                st.error(f"Registration Failed: {e}")
        
        st.markdown("---")
        if st.button("Already have an account? Log in here", key="go_to_login"):
            st.session_state.auth_mode = "login"
            st.rerun()

    st.stop()

# --- MAIN ENGINE INTERFACE (Runs if logged in) ---
with st.sidebar:
    st.markdown(f"👤 **OPERATOR:**\n`{st.session_state.user.email}`")
    st.markdown("---")
    if st.button("🚪 TERMINATE SESSION", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

st.title("🔥 Social Media Booster Engine")
st.markdown("Convert raw thoughts and conceptual fragments into structured, high-performing text output.")

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
