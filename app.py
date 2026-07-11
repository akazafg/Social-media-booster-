import streamlit as st
from supabase import create_client, Client
from openai import OpenAI
from st_paywall import add_auth

# 1. Page Configuration
st.set_page_config(page_title="Social Media Booster", layout="wide", page_icon="🔥")
st.title("🔥 Social Media Booster SaaS")

# 2. THE SUBSCRIPTION PAYWALL GATE
try:
    add_auth(
        required=True,
        login_button_text="Login with Google to start boosting",
        payment_button_text="Subscribe to Unlock Premium Engine",
    )
except Exception as e:
    st.error("Authentication setup pending. Please provide your Stripe and Google Client secrets.")
    st.stop()

# ----------------------------------------------------
# EVERYTHING BELOW THIS LINE IS LOCKED BEHIND THE PAYWALL
# ----------------------------------------------------
st.success(f"🎟️ Active Subscription Verified! Welcome back, {st.session_state.email}")

# 3. Database & AI Connections
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    
    supabase: Client = create_client(supabase_url, supabase_key)
    client = OpenAI(api_key=openai_api_key)
except Exception as e:
    st.error("Missing core API secrets in Streamlit Cloud Settings panel.")
    st.stop()

# 4. App UI Layout
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
            with st.spinner("Analyzing viral hooks and formatting..."):
                try:
                    system_prompt = "You are an elite growth marketer and viral ghostwriter."
                    user_prompt = f"Optimize this text: '{raw_text}' using the '{tone_style}' framework for LinkedIn and X."
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    
                    boosted_content = response.choices[0].message.content
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
