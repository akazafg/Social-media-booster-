import streamlit as st
from supabase import create_client, Client
import urllib.request
import urllib.parse
import json

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
st.markdown("Upload your market screenshot layout. The engine will read the image directly to analyze technical trends.")

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
    
    execute_vision = st.button("⚡ EXECUTE IMAGE VISION ANALYSIS", use_container_width=True)

with col2:
    st.markdown("### 📤 ENGINE EVALUATION VERDICT")
    
    if uploaded_chart is not None:
        st.image(uploaded_chart, caption="Ingested Market Chart Target Layout", use_container_width=True)
    else:
        st.info("System Standby: Awaiting valid graphic chart array ingestion.")

    if "vision_output" not in st.session_state:
        st.session_state.vision_output = ""

    if execute_vision:
        if uploaded_chart is None:
            st.warning("Analysis Halted: Please upload a chart screenshot image first so the vision engine can read it.")
        else:
            with st.spinner("Vision engine scanning chart pixels directly..."):
                try:
                    # 1. Convert the uploaded image into an absolute proxy image URL that Pollinations Vision can read
                    image_bytes = uploaded_chart.getvalue()
                    
                    # We upload to an open, secure imagery proxy pipeline
                    upload_url = "https://tmpfiles.org/api/v1/upload"
                    
                    # Boundary setting for raw multi-part form data processing without heavy external libraries
                    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
                    payload = []
                    payload.append(f"--{boundary}".encode())
                    payload.append(f'Content-Disposition: form-data; name="file"; filename="{uploaded_chart.name}"'.encode())
                    payload.append(f'Content-Type: {uploaded_chart.type}'.encode())
                    payload.append(b'')
                    payload.append(image_bytes)
                    payload.append(f"--{boundary}--".encode())
                    payload.append(b'')
                    
                    req_body = b'\r\n'.join(payload)
                    
                    upload_req = urllib.request.Request(
                        upload_url, 
                        data=req_body, 
                        headers={
                            'Content-Type': f'multipart/form-data; boundary={boundary}',
                            'User-Agent': 'Mozilla/5.0'
                        }
                    )
                    
                    with urllib.request.urlopen(upload_req) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                    
                    # Extract the temporary public image path URL
                    raw_file_url = res_data["data"]["url"]
                    accessible_image_url = raw_file_url.replace("https://tmpfiles.org/", "https://tmpfiles.org/dl/")
                    
                    # 2. Feed the absolute image path directly into the Multimodal Vision API Core
                    system_instruction = (
                        f"Analyze this uploaded chart image for the {market_context} market. "
                        "Look at the candles, trend directions, and structure. "
                        "You must begin your response exactly with one of these lines: "
                        "'🚨 RECOMMENDATION: BUY' or '🚨 RECOMMENDATION: SELL' or '🚨 RECOMMENDATION: HOLD'. "
                        "Then, list 2 clear reasons based on the actual visual candles/lines seen in the image."
                    )
                    
                    encoded_instruction = urllib.parse.quote(system_instruction)
                    encoded_img_url = urllib.parse.quote(accessible_image_url)
                    
                    # Combined vision pipeline endpoint
                    vision_endpoint = f"https://text.pollinations.ai/{encoded_instruction}?image={encoded_img_url}&model=p1"
                    
                    vision_req = urllib.request.Request(vision_endpoint, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(vision_req) as vision_res:
                        raw_verdict = vision_res.read().decode('utf-8')
                    
                    st.session_state.vision_output = raw_verdict
                    
                    # Database tracking log logic
                    db_payload = {
                        "user_input": f"Vision Scanned Market: {market_context}",
                        "ai_output": raw_verdict,
                        "platform": "Vision Analyzer Core"
                    }
                    supabase.table("generated_posts").insert(db_payload).execute()
                    
                except Exception as e:
                    st.error(f"Vision Processing Error: Make sure your internet connection is active. Details: {e}")

    if st.session_state.vision_output:
        st.success("TACTICAL STRATEGY EVALUATION COMPLETE")
        st.markdown(st.session_state.vision_output)
