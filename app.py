import streamlit as st
from supabase import create_client, Client
import urllib.request
import json

# 1. Page Configuration
st.set_page_config(page_title="BoostCore Auto-Poster", layout="wide", page_icon="🤖")

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
    st.title("🤖 BoostCore Automated Portal")
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

# --- MAIN AUTOMATED TERMINAL ---
st.title("🖥️ Mainframe: Instant Cross-Posting Engine")
st.markdown("Paste your TikTok link below. The app will automatically post it to your connected external platforms instantly.")

col1, col2 = st.columns([5, 6], gap="large")

with col1:
    st.markdown("### 📥 LINK INGESTION")
    tiktok_url = st.text_input("TikTok Video URL:", value="https://www.tiktok.com/@username/video/123456789")
    hype_message = st.text_area("Post Caption:", value="🔥 New video dropped! Watch, like, and follow right now!")
    
    # The automatic blast trigger button
    execute_blast = st.button("🚀 LAUNCH AUTOMATIC POSTING", use_container_width=True)

with col2:
    st.markdown("### 📡 LIVE NETWORK DEPLOYMENT LOGS")
    
    if execute_blast:
        full_post_text = f"{hype_message}\n\n🎬 Watch Link: {tiktok_url}"
        st.info("🔄 Connecting to external platform servers...")

        # 🎯 AUTOMATIC POSTING ROUTINE 1: DISCORD
        if "DISCORD_WEBHOOK_URL" in st.secrets and st.secrets["DISCORD_WEBHOOK_URL"]:
            try:
                payload = {"content": full_post_text}
                req = urllib.request.Request(
                    st.secrets["DISCORD_WEBHOOK_URL"],
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla"},
                    method="POST"
                )
                urllib.request.urlopen(req)
                st.success("✅ DISCORD: Automatically posted to your server channel!")
            except Exception as e:
                st.error(f"Discord Auto-Post Failed: {e}")
        else:
            st.warning("⚠️ Discord skipped: No webhook URL added to Streamlit Secrets.")

        # 🎯 AUTOMATIC POSTING ROUTINE 2: TELEGRAM
        if "TELEGRAM_BOT_TOKEN" in st.secrets and "TELEGRAM_CHAT_ID" in st.secrets:
            try:
                token = st.secrets["TELEGRAM_BOT_TOKEN"]
                chat_id = st.secrets["TELEGRAM_CHAT_ID"]
                telegram_url = f"https://api.telegram.com/bot{token}/sendMessage"
                
                payload = {"chat_id": chat_id, "text": full_post_text}
                req = urllib.request.Request(
                    telegram_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                urllib.request.urlopen(req)
                st.success("✅ TELEGRAM: Automatically posted to your Telegram channel!")
            except Exception as e:
                st.error(f"Telegram Auto-Post Failed: {e}")
        else:
            st.warning("⚠️ Telegram skipped: Keys missing from Streamlit Secrets.")

        # Save record to Supabase logs
        try:
            supabase.table("generated_posts").insert({
                "user_input": f"Auto-Post: {tiktok_url}",
                "ai_output": hype_message,
                "platform": "Automated Webhook V2"
            }).execute()
        except:
            pass
            
        st.balloons()
    else:
        st.info("System Idle: Ready to automatically transmit link assets.")
