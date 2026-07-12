import streamlit as st
from supabase import create_client, Client
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="BoostCore Launchpad", layout="wide", page_icon="🚀")

# 2. Database & Auth Connection
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("DATABASE ERROR: Missing core API secrets in Streamlit Cloud panel.")
    st.stop()

# Track Session Authentication
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("🚀 BoostCore Portal")
    email_input = st.text_input("System Email:")
    pwd_input = st.text_input("Passcode:", type="password")
    if st.button("Log In", use_container_width=True):
        try:
            res = supabase.auth.sign_in_with_password({"email": email_input, "password": pwd_input})
            st.session_state.user = res.user
            st.rerun()
        except:
            st.error("Access Denied.")
    st.stop()

# --- MAIN INTERFACE ---
st.title("🖥️ Mainframe: Instant Share Launchpad")
st.markdown("Paste your TikTok link below to instantly prepare your viral cross-promotion hooks.")

col1, col2 = st.columns([5, 6], gap="large")

with col1:
    st.markdown("### 📥 LINK INPUT")
    tiktok_url = st.text_input("Paste TikTok Video Link:", value="https://www.tiktok.com/@username/video/123456789")
    caption = st.text_area("Hype Caption:", value="🔥 Check out the new video right now! Drop a like and follow!")
    
    generate = st.button("⚡ PREPARE LAUNCH LINKS", use_container_width=True)

with col2:
    st.markdown("### 📤 INSTANT SHARE HUB")
    
    if generate:
        full_text = f"{caption}\n\n🎬 Watch here: {tiktok_url}"
        encoded_text = urllib.parse.quote(full_text)
        encoded_url = urllib.parse.quote(tiktok_url)
        
        st.success("✅ Launch links generated! Click below to push your link out instantly:")
        
        # Grid layout for sharing actions
        st.markdown(f"### [📬 Launch WhatsApp Share](https://api.whatsapp.com/send?text={encoded_text})")
        st.markdown(f"### [🐦 Launch X / Twitter Share](https://twitter.com/intent/tweet?text={encoded_text})")
        st.markdown(f"### [🔵 Launch Facebook Share](https://www.facebook.com/sharer/sharer.php?u={encoded_url})")
        
        # Log to Supabase
        try:
            supabase.table("generated_posts").insert({
                "user_input": f"Launchpad: {tiktok_url[:30]}",
                "ai_output": caption,
                "platform": "Zero-Setup Hub"
            }).execute()
        except:
            pass
    else:
        st.info("System Ready: Input your video link to activate the sharing launchpad.")
