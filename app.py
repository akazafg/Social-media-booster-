import streamlit as st
from supabase import create_client, Client
import urllib.request
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="BoostCore Vision Analyzer", layout="wide", page_icon="📈")

# 2. Database & Auth Connection
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("DATABASE ERROR: Missing core API secrets in Streamlit Cloud Settings panel.")
    st.stop()

# Track session routing states
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION PORTAL ---
if st.session_state.user is None:
    st.title("📈 BoostCore Vision Terminal")
    st.markdown("⚡ *Analyze chart structures and extract instantaneous tactical execution indicators.*")
    st.markdown("---")

    if st.session_state.auth_mode == "login":
        st.markdown("### 🔑 Log in to your analyzer terminal")
        login_email = st.text_input("Email*", key="login_email")
        login_password = st.text_input("Password*", type="password", key="login_pwd")
        
        if st.button("Log In", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error("ACCESS DENIED: Invalid credentials or unverified profile.")
        
        st.markdown("---")
        if st.button("Not registered? Create an account", key="go_to_signup"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    else:
        st.markdown("### 📝 Register your profile")
        signup_email = st.text_input("Email Address*", key="signup_email")
        signup_password = st.text_input("Password* (6+ characters)", type="password", key="signup_pwd")
        
        if st.button("Register Account", use_container_width=True):
            try:
                res = supabase.auth.sign_up({"email": signup_email, "password": signup_password})
                st.success("📩 VERIFICATION LINK SENT! Check your inbox to authorize your terminal.")
            except Exception as e:
                st.error(f"Registration Failed: {e}")
        
        st.markdown("---")
        if st.button("Already have an account? Log in", key="go_to_login"):
            st.session_state.auth_mode = "login"
            st.rerun()
    st.stop()

# --- MAIN TRADING ANALYZER INTERFACE (Logged In) ---
with st.sidebar:
    st.markdown(f"👤 **OPERATOR:**\n`{st.session_state.user.email}`")
    st.markdown("---")
    if st.button("🚪 TERMINATE SESSION", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

st.title("🖥️ Mainframe: Market Analysis Pipeline")
st.markdown("Upload your market screenshot layout and input visual behaviors to output immediate technical direction commands.")

col1, col2 = st.columns([5, 6], gap="large")

with col1:
    st.markdown("### 📥 CHART DATA INGESTION")
    
    uploaded_chart = st.file_uploader(
        "Upload Chart Screenshot (PNG, JPG, JPEG):", 
        type=["png", "jpg", "jpeg"]
    )
    
    market_context = st.text_input(
        "Market / Asset Class Name:", 
        value="OTC Crypto Market"
    )
    
    chart_description = st.text_area(
        "Describe what you see (Candle color, indicators, support/resistance lines):",
        height=120,
        placeholder="e.g., Massive green candle breaking through resistance line, RSI is at 65, moving averages crossing upward..."
    )
    
    execute_vision = st.button("⚡ EXECUTE AUTOMATED CHART ANALYSIS", use_container_width=True)

with col2:
    st.markdown("### 📤 ENGINE EVALUATION VERDICT")
    
    if uploaded_chart is not None:
        st.image(uploaded_chart, caption="Ingested Market Chart Target Layout", use_container_width=True)
    else:
        st.info("System Standby: Awaiting valid graphic chart array ingestion.")

    if "vision_output" not in st.session_state:
        st.session_state.vision_output = ""

    if execute_vision:
        if not chart_description.strip():
            st.warning("Analysis Halted: Please describe the technical behaviors seen on your chart.")
        else:
            with st.spinner("Processing structural indicators..."):
                try:
                    # Clean, non-restricted prompt layout
                    structural_directive = (
                        f"Analyze this {market_context} trade setup configuration. User description: '{chart_description}'. "
                        "Give a quick technical trend overview. Your analysis must begin exactly with one of these options: "
                        "'🚨 RECOMMENDATION: BUY' or '🚨 RECOMMENDATION: SELL' or '🚨 RECOMMENDATION: HOLD'. "
                        "Then list 2 quick reasons supporting that option."
                    )
                    
                    encoded_prompt = urllib.parse.quote(structural_directive)
                    api_endpoint = f"https://text.pollinations.ai/{encoded_prompt}"
                    
                    req = urllib.request.Request(api_endpoint, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        raw_verdict = response.read().decode('utf-8')
                    
                    st.session_state.vision_output = raw_verdict
                    
                    # Database tracking log logic
                    db_payload = {
                        "user_input": f"Market: {market_context} | Description: {chart_description}",
                        "ai_output": raw_verdict,
                        "platform": "Vision Analyzer Core"
                    }
                    supabase.table("generated_posts").insert(db_payload).execute()
                    
                except Exception as e:
                    st.error(f"Processing Defect: {e}")

    if st.session_state.vision_output:
        st.success("TACTICAL STRATEGY EVALUATION COMPLETE")
        st.markdown(st.session_state.vision_output)
