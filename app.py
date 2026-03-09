import streamlit as st
import random
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# --- 1. AUTHENTICATION & SETUP ---
load_dotenv()

st.set_page_config(
    page_title="Think With Shane",  # Replace with your new name
    page_icon="💠",                 # Drop any emoji you want right here
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Supabase
@st.cache_resource
def init_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.error("Database keys missing. Check your .env file.")
        st.stop()
    return create_client(url, key)

supabase = init_supabase()

# --- 2. THE VAULT RETRIEVAL SYSTEM ---
def fetch_daily_shift(category):
    try:
        response = supabase.table('reality_shifts').select("*").eq('category', category).order('created_at', desc=True).limit(1).execute()
        if response.data:
            return response.data[0]
        else:
            return None 
    except Exception as e:
        print(f"Database error: {e}")
        return None

# --- 3. STATE MANAGEMENT ---
categories = ["Psychology", "Human Systems", "Physics", "Biology"]

if 'current_category' not in st.session_state:
    st.session_state.current_category = random.choice(categories)

# --- 4. THE COLOR THEMES ---
themes = {
    "Biology": {"orb1": "rgba(127, 255, 212, 0.15)", "orb2": "rgba(80, 200, 120, 0.12)", "primary": "#7FFFD4", "secondary": "#50C878"},
    "Psychology": {"orb1": "rgba(181, 126, 220, 0.15)", "orb2": "rgba(147, 112, 219, 0.12)", "primary": "#B57EDC", "secondary": "#9370DB"}, 
    "Physics": {"orb1": "rgba(0, 255, 255, 0.12)", "orb2": "rgba(65, 105, 225, 0.15)", "primary": "#00FFFF", "secondary": "#4169E1"},
    "Human Systems": {"orb1": "rgba(255, 191, 0, 0.12)", "orb2": "rgba(255, 69, 0, 0.12)", "primary": "#FFBF00", "secondary": "#FF4500"}
}

active_theme = themes[st.session_state.current_category]

# --- 5. CLEAN CSS INJECTION ---
st.markdown(f"""
    <style>
    
    /* 1. The Breathing Background */
    .stApp {{ 
        background: linear-gradient(-45deg, #020403, #061410, #020403, #041214);
        background-size: 400% 400%;
        background-attachment: fixed;
        animation: ambientGlow 18s ease infinite;
    }}
    @keyframes ambientGlow {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    
    /* 2. THE BRANDING ASSASSIN (Silent Method) */
    /* This keeps the header active (so the sidebar works) but hides the icons */
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0) !important; }}
    [data-testid="stHeaderActionElements"] {{ opacity: 0 !important; pointer-events: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    footer {{ display: none !important; }}
    .viewerBadge_container {{ display: none !important; }}

    /* Make the Sidebar Toggle Button stand out */
    button[data-testid="stSidebarCollapseButton"] {{
        color: {active_theme['primary']} !important;
    }}

    /* 3. The Dynamic Orbs */
    .orb-1 {{
        position: fixed; top: 15%; left: 5%; width: 50vw; height: 50vw;
        background-color: {active_theme['orb1']}; filter: blur(140px);
        border-radius: 50%; z-index: 0; pointer-events: none;
        animation: float 12s infinite alternate ease-in-out;
    }}
    .orb-2 {{
        position: fixed; bottom: -10%; right: 5%; width: 60vw; height: 60vw;
        background-color: {active_theme['orb2']}; filter: blur(160px);
        border-radius: 50%; z-index: 0; pointer-events: none;
        animation: floatReverse 15s infinite alternate ease-in-out;
    }}
    @keyframes float {{ 0% {{ transform: translate(0px, 0px); }} 100% {{ transform: translate(60px, -60px); }} }}
    @keyframes floatReverse {{ 0% {{ transform: translate(0px, 0px); }} 100% {{ transform: translate(-70px, 70px); }} }}

    /* 4. Text Content */
    .content-wrapper {{ position: relative; z-index: 10; padding: 0 20px; }}
    [data-testid="stAppViewBlockContainer"] {{ background-color: transparent !important; padding-top: 2rem; }}

    .hook-text {{ color: {active_theme['primary']}; text-shadow: 0 0 25px {active_theme['orb1']}; font-size: 2.3rem; font-weight: 700; text-align: center; margin-top: 3vh; margin-bottom: 60px; line-height: 1.4; font-family: 'Georgia', serif; }}
    .body-text {{ color: #F0F0F0; font-size: 1.25rem; line-height: 1.9; font-family: 'Helvetica Neue', sans-serif; margin-bottom: 50px; }}
    .section-title {{ color: {active_theme['secondary']}; font-size: 1.5rem; font-family: 'Georgia', serif; margin-top: 30px; margin-bottom: 20px; text-shadow: 0 0 15px {active_theme['orb2']}; border-bottom: 1px solid {active_theme['orb2']}; padding-bottom: 10px; text-align: center; }}
    .sign-off {{ color: {active_theme['primary']}; text-align: center; font-size: 1.1rem; margin-top: 60px; margin-bottom: 40px; font-style: italic; }}

    /* 5. Button Styling */
    button[kind="primary"] {{
        background-color: {active_theme['orb1']} !important;
        border: 1px solid {active_theme['primary']} !important;
        color: {active_theme['primary']} !important;
    }}
    button[kind="secondary"] {{
        background-color: rgba(3,6,4,0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #A0A0A0 !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='orb-1'></div><div class='orb-2'></div>", unsafe_allow_html=True)

# --- 6. THE DYNAMIC SIDEBAR ---
with st.sidebar:
    st.markdown(f"<h3 style='color: {active_theme['primary']}; text-shadow: 0 0 10px {active_theme['orb1']}; text-align: center; transition: color 1.5s ease;'>Get the Spark</h3>", unsafe_allow_html=True)
    st.caption("Subscribe for the daily shift.")
    st.text_input("Email (Full Read):", placeholder="Enter email...")
    st.text_input("SMS (Quick Hint):", placeholder="Enter phone #...")
    st.button("Subscribe", key="sub_btn", use_container_width=True)
    
    st.divider()
    
    # NEW MISSION STATEMENT SECTION
    st.markdown(f"<h3 style='color: {active_theme['secondary']}; text-shadow: 0 0 10px {active_theme['orb2']}; text-align: center; transition: color 1.5s ease;'>The Mission</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style='color: #D3D3D3; font-size: 0.95rem; line-height: 1.7; text-align: justify; padding: 10px 5px; font-family: "Helvetica Neue", sans-serif;'>
        This space is designed to make you think. Every single day, we hunt down bleeding-edge academic research and translate it into a reality shift. <br><br>
        The goal? To help you discover what you were never taught, question the systems you blindly accept, and spark high-level conversations with the people around you. 
        </div>
    """, unsafe_allow_html=True)
        
    st.divider()
    
    st.markdown("<div class='brand-text'>designed and built by<br><b>thinkwithshane</b></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="x-logo-container" style="text-align: center; margin-top: 15px;">
            <a href="YOUR_X_LINK_HERE" target="_blank">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 22.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
            </a>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='content-wrapper'>", unsafe_allow_html=True)

# --- 7. THE NATIVE NAVIGATION ROW ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Psychology", type="primary" if st.session_state.current_category == "Psychology" else "secondary", use_container_width=True):
        st.session_state.current_category = "Psychology"
        st.rerun()
with col2:
    if st.button("Human Systems", type="primary" if st.session_state.current_category == "Human Systems" else "secondary", use_container_width=True):
        st.session_state.current_category = "Human Systems"
        st.rerun()
with col3:
    if st.button("Physics", type="primary" if st.session_state.current_category == "Physics" else "secondary", use_container_width=True):
        st.session_state.current_category = "Physics"
        st.rerun()
with col4:
    if st.button("Biology", type="primary" if st.session_state.current_category == "Biology" else "secondary", use_container_width=True):
        st.session_state.current_category = "Biology"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- 8. FETCH AND RENDER THE LIVE CONTENT ---
vault_data = fetch_daily_shift(st.session_state.current_category)

if vault_data:
    st.markdown(f"<div class='hook-text'>{vault_data['hook']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-text'><div class='section-title'>The Facts</div>{vault_data['mechanism']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-text'><div class='section-title'>So What?</div>{vault_data['shift']}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='hook-text'>The engine is currently hunting the archives for {st.session_state.current_category}.</div>", unsafe_allow_html=True)
    st.markdown("<div class='body-text'><div class='section-title'>Status: Pending</div>The AI Editor has not yet published an essay for this discipline. It will wake up tonight at 2:00 AM to scan the global research networks.</div>", unsafe_allow_html=True)
    st.markdown("<div class='body-text'><div class='section-title'>Next Steps</div>Check back tomorrow morning to see what reality it shatters next.</div>", unsafe_allow_html=True)

# Dynamic Sign-off
if st.session_state.current_category in ["Psychology", "Human Systems"]:
    st.markdown(f"<div class='sign-off'>Think about that. See you tomorrow.</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='sign-off'>Knowledge acquired. See you tomorrow.</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
