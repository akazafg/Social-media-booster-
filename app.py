import streamlit as st
from supabase import create_client, Client
import urllib.request
import urllib.parse

# 1. Page Configuration & Elite Styling
st.set_page_config(page_title="Social Media Booster", layout="wide", page_icon="🔥")

# Injecting Custom Legendary CSS
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d0e15 0%, #06070a 100%);
        color: #e2e8f0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Neon Title Styling */
    .legend-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00dfd8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(121, 40, 202, 0.3);
    }
    
    .legend-subtitle {
        color: #8a99ad;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    /* Glassmorphism Cards */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(18, 20, 32, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Glowing Action Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #7928ca 0%, #ff007f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(255, 0, 127, 0.6) !important;
    }
    
    /* Input Fields Matrix Styling */
    textarea, input, select {
        background-color: #0d0f17 !important;
        color: #00dfd8 !important;
        border: 1px solid #2d3142 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
    }
    
    textarea:focus, input:focus {
        border-color: #00dfd8 !important;
        box-shadow: 0 0 10px rgba(0, 223, 216, 0.3) !important;
    }
    
    /* Tabs Customization */
    button[data-baseweb="tab"] {
        color: #8a99ad !important;
        font-size: 1.1rem !important;
    }
    button[aria-selected="true"] {
        color: #00dfd8 !important;
        border-bottom-color: #00dfd8 !important;
    }
    </style>
""", unsafe_allowed_html=True)

# 2. Database & Auth Connection
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("Missing core API secrets in Streamlit Cloud Settings panel.")
    st.stop()

if "user" not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION INTERFACE ---
if st.session_state.user is None:
    with st.sidebar:
        st.markdown("### ⚡ ENGINE CORE")
        st.markdown("🌐 STATUS: `ONLINE`")
        st.markdown("🔒 CODES: `ENCRYPTED`")
        st.markdown("---")
        st.markdown("### 🚀 PREMIUM EXTENSION")
        st.info("🌟 **LAUNCHING SEPT 2026**\n\nUnlock Tier-1 algorithms, neural image matrices, and industrial automation pipelines.")

    st.markdown('<h1 class="legend-title">BOOSTER ARCHITECTURE</h1>', unsafe_allowed_html=True)
    st.markdown('<p class="legend-subtitle">Access the elite content optimization mainframe.</p>', unsafe_allowed_html=True)

    auth_tab1, auth_tab2 = st.tabs(["🔑 ACCESS ACCOUNT", "📝 INITIALIZE PROFILE"])

    with auth_tab1:
        login_email = st.text_input("ENTER EMAIL", key="login_email_input")
        login_password = st.text_input("ENTER PASSWORD", type="password", key="login_pwd_input")
        if st.button("AUTHORIZE CONNECTION", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error("ACCESS DENIED: Invalid credentials.")

    with auth_tab2:
        signup_email = st.text_input("REGISTER EMAIL", key="signup_email_input")
        signup_password = st.text_input("CREATE SECURE PASSWORD (6+ Chars)", type="password", key="signup_pwd_input")
        if st.button("GENERATE NEW ACCESS PROFILE", use_container_width=True):
            try:
                res = supabase.auth.sign_up({"email": signup_email, "password": signup_password})
                st.success("✅ Mainframe account created! Sign In immediately.")
            except Exception as e:
                st.error(f"Initialization Failed: {e}")

    st.stop()

# --- MAIN APP INTERFACE (Only runs if logged in) ---
with st.sidebar:
    st.markdown(f"⚡ **OPERATOR:**\n`{st.session_state.user.email}`")
    st.markdown("---")
    st.markdown("### 🚀 PREMIUM TIERS")
    st.info("🌟 **RELEASING IN 2 MONTHS**\n\nPrepare for heavy-duty volume metrics and raw network amplification protocols.")
    st.markdown("---")
    if st.button("🚪 TERMINATE SESSION", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

st.markdown('<h1 class="legend-title">SOCIAL BOOSTER ENGINE</h1>', unsafe_allowed_html=True)
st.markdown('<p class="legend-subtitle">Convert raw thought sequences into global authority matrices.</p>', unsafe_allowed_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 RAW INGESTION CORE")
    raw_text = st.text_area(
        "Input unoptimized sequence concept:",
        height=200,
        placeholder="Type raw ideas, stats, or metrics here..."
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
            with st.spinner("Processing neural matrices via free engine..."):
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
