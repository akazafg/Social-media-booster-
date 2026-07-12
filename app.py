import streamlit as st
from supabase import create_client, Client
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="BoostCore Growth Hub", layout="wide", page_icon="🚀")

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
    st.title("🚀 BoostCore Organic Growth Hub")
    st.markdown("⚡ *Cross-promote your video assets across multiple platforms to scale views.*")
    st.markdown("---")

    if st.session_state.auth_mode == "login":
        st.markdown("### 🔑 Log in to your marketing command terminal")
        login_email = st.text_input("Email*", key="login_email")
        login_password = st.text_input("Password*", type="password", key="login_pwd")
        
        if st.button("Log In", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error("ACCESS DENIED: Invalid credentials.")
        st.stop()

# --- MAIN ENGINE INTERFACE ---
with st.sidebar:
    st.markdown(f"👤 **OPERATOR:**\n`{st.session_state.user.email}`")
    st.markdown("---")
    st.markdown("### 📢 PROMO GOAL")
    promo_style = st.selectbox("Select Blast Angle:", ["🔥 Direct Heat / Hype", "💿 Out Now / Streaming", "👀 Behind The Scenes"])
    
    if st.button("🚪 LOG OUT", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

st.title("🖥️ Mainframe: Multi-Platform Cross-Promotion Panel")
st.markdown("Paste your video link below to parse the media asset and deploy your text templates instantly.")

col1, col2 = st.columns([5, 6], gap="large")

with col1:
    st.markdown("### 📥 TIKTOK SOURCE ELEMENT")
    tiktok_link = st.text_input("TikTok Video Link URL:", value="https://www.tiktok.com/@username/video/123456789")
    artist_tag = st.text_input("Your Artist / Handle Profile Name:", value="Dan Lee")
    
    execute_build = st.button("⚡ EXECUTE CAMPAIGN INJECTION", use_container_width=True)

with col2:
    st.markdown("### 📤 LIVE DISTRIBUTION ENGINE")
    
    if execute_build:
        # Determine unique promotional strings based on selection parameters
        if promo_style == "🔥 Direct Heat / Hype":
            caption_template = f"🔥 Yo! The new drip from {artist_tag} is moving heavy right now. Tap the link to view, drop a like, and follow up! 👇\n{tiktok_link}"
        elif promo_style == "💿 Out Now / Streaming":
            caption_template = f"💿 The wait is over. The official video from {artist_tag} is live right now! Pull up, show love, and share it across! 👇\n{tiktok_link}"
        else:
            caption_template = f"👀 Real behind the scenes energy from {artist_tag}. Hit the video link to tap into the movement directly! 👇\n{tiktok_link}"
            
        # URL safe text formatting conversion for sharing sheets
        encoded_caption = urllib.parse.quote(caption_template)
        
        st.success("🎯 CROSS-PROMOTION TEMPLATE DESIGN COMPLETE")
        st.markdown("#### 📝 Copy Your Generated Copytext:")
        st.text_area("Ready-to-Post Text:", value=caption_template, height=100)
        
        st.markdown("#### ⚡ Launch One-Click Share Sheets:")
        
        # Streamlit actionable native buttons to fire open target destination apps with text pre-loaded
        st.markdown(f"[📬 Share Straight to WhatsApp](https://api.whatsapp.com/send?text={encoded_caption})")
        st.markdown(f"[🐦 Tweet to X Pipeline](https://twitter.com/intent/tweet?text={encoded_caption})")
        st.markdown(f"[🔵 Post to Facebook Communities](https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(tiktok_link)})")
        
        st.markdown("---")
        st.info("💡 **Strategy Track:** Open your app link on your phone. Hit these share links to pop the apps open directly, drop the pre-formatted text instantly into group chats and timelines, and watch the traffic compound!")

        # Log ad activity metrics securely to database table
        try:
            db_payload = {
                "user_input": f"Cross-Promoted Track: {artist_tag}",
                "ai_output": f"Style: {promo_style}",
                "platform": "Organic Growth Hub"
            }
            supabase.table("generated_posts").insert(db_payload).execute()
        except Exception:
            pass
    else:
        st.info("System Standby: Input your TikTok video properties to compile your organic cross-platform assets.")
