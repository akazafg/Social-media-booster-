import streamlit as st
from supabase import create_client, Client
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="BoostCore Universal Hub", layout="wide", page_icon="🚀")

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
    st.title("🚀 BoostCore Multi-Network Hub")
    st.markdown("⚡ *Cross-promote your music and videos to maximize views and followers.*")
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
st.markdown("Paste your source links below to generate text templates and deploy your cross-platform sharing pipeline.")

col1, col2 = st.columns([5, 6], gap="large")

with col1:
    st.markdown("### 📥 VIDEO SOURCE ELEMENTS")
    source_link = st.text_input("Your Track / Video URL Link:", value="https://www.tiktok.com/@username/video/123456789")
    artist_tag = st.text_input("Your Artist Handle Name:", value="Dan Lee")
    
    execute_build = st.button("⚡ EXECUTE ALL PLATFORM TAGS", use_container_width=True)

with col2:
    st.markdown("### 📤 LIVE DISTRIBUTION PIPELINES")
    
    if execute_build:
        # Determine promo caption structures based on selection parameters
        if promo_style == "🔥 Direct Heat / Hype":
            caption_template = f"🔥 Yo! The new movement from {artist_tag} is heavy right now. Tap the link to view, drop a like, and follow up! 🎧👇\n{source_link}"
            hashtags = "#ukdrip #hiphop #newmusic #trending"
        elif promo_style == "💿 Out Now / Streaming":
            caption_template = f"💿 The wait is over. The official drop from {artist_tag} is live! Pull up, show love, and share it across! 🚀👇\n{source_link}"
            hashtags = "#outnow #independentartist #musicvideo #rap"
        else:
            caption_template = f"👀 Real behind the scenes energy from {artist_tag}. Hit the link to tap into the studio layout directly! 🎬👇\n{source_link}"
            hashtags = "#bts #studioflow #artistlife #hiphopvibe"
            
        full_text_with_tags = f"{caption_template}\n\n{hashtags}"
        encoded_caption = urllib.parse.quote(full_text_with_tags)
        
        st.success("🎯 CROSS-PROMOTION TEMPLATE GENERATED")
        st.markdown("#### 📝 Copy Text & Tags for TikTok/YouTube Shorts:")
        st.text_area("Ready-to-Use Copytext:", value=full_text_with_tags, height=130)
        
        st.markdown("#### ⚡ Launch Quick-Action Portals:")
        
        # 1. Text-sharing automation portals
        st.markdown(f"[📬 Share to WhatsApp Groups](https://api.whatsapp.com/send?text={encoded_caption})")
        st.markdown(f"[🐦 Post to X Timeline](https://twitter.com/intent/tweet?text={encoded_caption})")
        st.markdown(f"[🔵 Share to Facebook Community](https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(source_link)})")
        
        st.markdown("---")
        # 2. Direct upload and promotion entry points for Video Hubs
        st.markdown("[🎵 Open TikTok Web Upload Portal](https://www.tiktok.com/tiktokstudio/upload)")
        st.markdown("[📺 Open YouTube Studio Upload Portal](https://studio.youtube.com/channel/videos/shorts)")
        
        st.markdown("---")
        st.info("💡 **Mobile Workflow Strategy:** Open this dashboard link on your mobile phone browser. Copy the generated text block above, hit the TikTok or YouTube links to open the upload pages instantly, drop your video file in, and paste the pre-made viral tags instantly!")

        # Log ad activity metrics securely to database table
        try:
            db_payload = {
                "user_input": f"Full Promo: {artist_tag}",
                "ai_output": f"Style: {promo_style}",
                "platform": "Universal Growth Engine"
            }
            supabase.table("generated_posts").insert(db_payload).execute()
        except Exception:
            pass
    else:
        st.info("System Standby: Input your track properties to compile your organic cross-platform distribution array.")
