import streamlit as st
from supabase import create_client, Client
import random

# 1. Page Configuration
st.set_page_config(page_title="BoostCore Viral Studio", layout="wide", page_icon="🎬")

# 2. Database & Auth Connection
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("DATABASE ERROR: Missing core API secrets in Streamlit Cloud panel.")
    st.stop()

# Session State Route Engine
if "user" not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION PORTAL ---
if st.session_state.user is None:
    st.title("🎬 BoostCore Viral Command Console")
    email_input = st.text_input("Enter Registered System Email:")
    pwd_input = st.text_input("Security Passcode:", type="password")
    if st.button("Authorize Console Access", use_container_width=True):
        try:
            res = supabase.auth.sign_in_with_password({"email": email_input, "password": pwd_input})
            st.session_state.user = res.user
            st.rerun()
        except:
            st.error("Invalid Command Credentials.")
    st.stop()

# --- MAIN VIRAL MATRIX ---
st.title("🖥️ Mainframe: Viral Script & Hook Blueprint Generator")
st.markdown("Type what your video is about. The engine will instantly format a psychological structural blueprint to keep viewers watching.")

with st.sidebar:
    st.markdown(f"👤 **USER:** `{st.session_state.user.email}`")
    st.markdown("---")
    video_style = st.selectbox("Select Content Tone:", ["🤫 Controversial / Shocking", "🧠 Educational / Mind-Blowing", "😂 High Entertainment / Relatable"])
    
    if st.button("🚪 DISCONNECT"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

col1, col2 = st.columns([5, 6], gap="large")

with col1:
    st.markdown("### 📥 VIDEO TOPIC INGESTION")
    video_topic = st.text_input("What happens in your video? (e.g., trying a crazy food, reacting to a trend):", value="testing a weird life hack")
    
    generate_blueprint = st.button("⚡ GENERATE VIRAL BLUEPRINT", use_container_width=True)

with col2:
    st.markdown("### 📤 ALGORITHM COMPLIANT BLUEPRINT")
    
    if generate_blueprint:
        # Internal logical arrays to construct retention frameworks
        if video_style == "🤫 Controversial / Shocking":
            hooks = [f"❌ Stop scrolling if you still do this. Let me show you why...", f"😳 I was completely lied to about this, and you probably are too."]
            comment_baits = "Drop your opinion below, am I completely wrong for this?"
        elif video_style == "🧠 Educational / Mind-Blowing":
            hooks = [f"🧠 The exact moment I realized this changed everything...", f"🤯 This looks completely fake, but it is 100% real. Look at this."]
            comment_baits = "Tell me in the comments if you knew about this before watching."
        else:
            hooks = [f"😂 Nobody talks about how awkward this actually is...", f"💀 I spent way too long making this, watch what happens at the end."]
            comment_baits = "Rate this video from 1-10 in the comments right now."

        chosen_hook = random.choice(hooks)
        
        st.success("🎯 Retention Blueprint Structured Successfully!")
        
        with st.container(border=True):
            st.subheader("🎬 Video Structure Blueprint")
            st.markdown(f"**⏱️ Seconds 0-2 (The Hook):**\n`{chosen_hook}`\n*(Overlay this exact text visually on the screen immediately!)*")
            st.markdown(f"**⏱️ Seconds 3-8 (The Core Body):**\n*Show the action related to '{video_topic}' dynamically. Keep video cuts every 1.5 seconds so viewers don't get bored.*")
            st.markdown(f"**⏱️ Seconds 9-12 (The Loop & Bait):**\n*Deliver the final reveal rapidly, then immediately cut the video so it repeats seamlessly.*")
            
            st.markdown("---")
            st.subheader("💬 Optimized TikTok Caption & Comment Bait")
            st.code(f"Wait until the ending... 🍿 {comment_baits} #fyp #trending #viral", language="text")

        # Save to logs securely
        try:
            db_payload = {
                "user_input": f"Topic: {video_topic}",
                "ai_output": chosen_hook,
                "platform": "Viral Blueprint Engine"
            }
            supabase.table("generated_posts").insert(db_payload).execute()
        except:
            pass
    else:
        st.info("System Standby: Awaiting video topic input to run blueprint processing.")
