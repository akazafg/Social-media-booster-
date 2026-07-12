import streamlit as st
from supabase import create_client, Client
import urllib.request
import json
import base64

# 1. Page Configuration
st.set_page_config(page_title="BoostCore OTC Terminal", layout="wide", page_icon="📈")

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
    st.title("📈 BoostCore OTC Scanner Portal")
    st.markdown("⚡ *Upload broker screenshots for direct visual trend extraction.*")
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

# --- MAIN OTC SCANNER INTERFACE (Logged In) ---
with st.sidebar:
    st.markdown(f"👤 **OPERATOR:**\n`{st.session_state.user.email}`")
    st.markdown("---")
    if st.button("🚪 TERMINATE SESSION", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

st.title("🖥️ Mainframe: OTC Tactical Extraction")
st.markdown("Upload your latest OTC chart screenshot layout. The vision pipeline handles pixel conversion locally.")

col1, col2 = st.columns([5, 6], gap="large")

with col1:
    st.markdown("### 📥 OTC CHART INGESTION")
    
    uploaded_chart = st.file_uploader(
        "Upload Broker Screenshot (PNG, JPG, JPEG):", 
        type=["png", "jpg", "jpeg"]
    )
    
    execute_vision = st.button("⚡ EXTRACT IMMEDIATE TACTICAL VERDICT", use_container_width=True)

with col2:
    st.markdown("### 📤 ENGINE EVALUATION VERDICT")
    
    if uploaded_chart is not None:
        st.image(uploaded_chart, caption="Ingested OTC Chart Array", use_container_width=True)
    else:
        st.info("System Standby: Awaiting valid graphic chart array ingestion.")

    if "vision_output" not in st.session_state:
        st.session_state.vision_output = ""

    if execute_vision:
        if uploaded_chart is None:
            st.warning("Analysis Halted: Please upload your OTC chart screenshot image first.")
        else:
            with st.spinner("Decoding image pixels securely..."):
                try:
                    # Direct local conversion to safe string data URI - completely prevents 404 site errors
                    image_bytes = uploaded_chart.getvalue()
                    base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
                    data_url = f"data:{uploaded_chart.type};base64,{base64_encoded}"
                    
                    system_instruction = (
                        "Analyze this uploaded broker chart screenshot closely. Look at the colors and recent candle momentum directions. "
                        "You must start your response exactly with one of these lines based on what you see: "
                        "'🚨 RECOMMENDATION: BUY (UP)' or '🚨 RECOMMENDATION: SELL (DOWN)' or '🚨 RECOMMENDATION: HOLD (NEUTRAL)'. "
                        "Then, write exactly two short bullet points explaining why."
                    )
                    
                    # Direct multi-modal text/image payload structural design
                    payload_data = {
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": system_instruction},
                                    {"type": "image_url", "image_url": {"url": data_url}}
                                ]
                            }
                        ],
                        "model": "p1",
                        "jsonMode": False
                    }
                    
                    api_endpoint = "https://text.pollinations.ai/"
                    req_json = json.dumps(payload_data).encode('utf-8')
                    
                    req = urllib.request.Request(
                        api_endpoint,
                        data=req_json,
                        headers={
                            'Content-Type': 'application/json',
                            'User-Agent': 'Mozilla/5.0'
                        }
                    )
                    
                    with urllib.request.urlopen(req) as response:
                        raw_verdict = response.read().decode('utf-8')
                    
                    st.session_state.vision_output = raw_verdict
                    
                    # Store log snapshot in database
                    db_payload = {
                        "user_input": "OTC Direct Base64 Vision Extraction Execution",
                        "ai_output": raw_verdict,
                        "platform": "Vision Analyzer Core"
                    }
                    supabase.table("generated_posts").insert(db_payload).execute()
                    
                except Exception as e:
                    st.error(f"Vision Connection Interface Timeout. Details: {e}")

    if st.session_state.vision_output:
        st.success("TACTICAL STRATEGY EVALUATION COMPLETE")
        st.markdown(st.session_state.vision_output)
