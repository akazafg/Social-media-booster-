import streamlit as st
from supabase import create_client, Client
import urllib.request
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Social Media Booster", layout="wide", page_icon="🔥")
st.title("🔥 Free Social Media Booster")

# 2. Database Connections (Using your free Supabase)
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("Missing core API secrets in Streamlit Cloud Settings panel.")
    st.stop()

# 3. App UI Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 Input Your Raw Post / Concept")
    raw_text = st.text_area(
        "What do you want to talk about?",
        height=200,
        placeholder="e.g., Just launched my website..."
    )
    
    tone_style = st.selectbox(
        "Choose Viral Tone Style:",
        ["Thought Leader (Analytical & Bold)", "Storyteller (Emotional & Hooks)", "The Growth Hacker (Punchy & Short)"]
    )
    
    boost_trigger = st.button("🚀 Boost Content Performance", use_container_width=True)

with col2:
    st.markdown("### 📤 High-Performance Outputs")
    if boost_trigger:
        if not raw_text.strip():
            st.warning("Please insert some text or an idea first.")
        else:
            with st.spinner("Analyzing viral hooks using free engine..."):
                try:
                    # Free Serverless AI Text Generation API
                    prompt = f"Optimize this text: '{raw_text}' using the '{tone_style}' framework for LinkedIn and X. Be an elite growth marketer."
                    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                    
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        boosted_content = response.read().decode('utf-8')
                    
                    st.success("Content Boost Complete!")
                    st.markdown(boosted_content)
                    
                    # Store data inside Supabase
                    db_data = {
                        "user_input": raw_text,
                        "ai_output": boosted_content,
                        "platform": tone_style
                    }
                    supabase.table("generated_posts").insert(db_data).execute()
                    
                except Exception as e:
                    st.error(f"Execution Error: {e}")
