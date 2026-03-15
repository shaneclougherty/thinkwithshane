import streamlit as st
import random
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# --- 1. AUTHENTICATION & SETUP ---
load_dotenv()

st.set_page_config(
    page_title="Think With Shane",  
    page_icon="💠",                 
    layout="wide", # Using wide layout helps fit 5 columns nicely on desktop
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
categories = ["Psychology", "Human History", "Physics", "Biology", "Technology"]

if 'current_category' not in st.session_state:
    st.session_state.current_category = random.choice(categories)

# --- 4. THE COLOR THEMES ---
themes = {
    "Psychology": {"orb1": "rgba(181, 126, 220, 0.15)", "orb2": "rgba(147, 112, 219, 0.12)", "primary": "#B57EDC", "secondary": "#9370DB"}, 
    "Human History": {"orb1": "rgba(255, 191, 0, 0.12)", "orb2": "rgba(255, 69, 0, 0.12)", "primary": "#FFBF00", "secondary": "#FF4500"},
    "Physics": {"orb1": "rgba(65, 105, 225, 0.15)", "orb2": "rgba(138, 43, 226, 0.12)", "primary": "#4169E1", "secondary": "#8A2BE2"},
    "Biology": {"orb1": "rgba(80, 200, 120, 0.15)", "orb2": "rgba(34, 139, 34, 0.12)", "primary": "#50C878", "secondary": "#228B22"},
    "Technology": {"orb1": "rgba(0, 255, 255, 0.15)", "orb2": "rgba(32, 178, 170, 0.12)", "primary": "#00FFFF", "secondary": "#20B2AA"}
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
    
    /* 2. BASE FRAMEWORK CLEANUP (Render Safe) */
    footer {{visibility: hidden !important; display: none !important;}}
    [data-testid="stHeader"] {{background: rgba(0,0,0,0) !important;}}
    [data-testid="stToolbar"] {{visibility: hidden !important; display: none !important;}}
    
    /* Protect the Sidebar Toggle */
    [data-testid="stSidebarCollapsedControl"] {{
        display: block !important;
        visibility: visible !important;
        z-index: 99999 !important;
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
    .content-wrapper {{ position: relative; z-index: 10; max-width: 800px; margin: 0 auto; padding: 0 20px; }}
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
    
    /* 6. Footer Branding Restoration */
    .brand-text {{ color: {active_theme['secondary']}; text-align: center; font-size: 0.9rem; margin-top: 40px; font-family: 'Courier New', monospace; text-shadow: 0 0 10px {active_theme['orb2']}; transition: color 1.5s ease; }}
    .x-logo-container a {{ color: {active_theme['primary']} !important; transition: all 0.3s ease; display: inline-block; padding: 10px; }}
    .x-logo-container a:hover {{ transform: scale(1.1); filter: drop-shadow(0 0 8px {active_theme['orb1']}); }}
    
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='orb-1'></div><div class='orb-2'></div>", unsafe_allow_html=True)

# --- 6. THE DYNAMIC SIDEBAR WITH LEAD CAPTURE ---
with st.sidebar:
    st.markdown(f"<h3 style='color: {active_theme['primary']}; text-shadow: 0 0 10px {active_theme['orb1']}; text-align: center; transition: color 1.5s ease;'>Get the Spark</h3>", unsafe_allow_html=True)
    st.caption("Subscribe for the daily shift.")
    
    email_input = st.text_input("Email (Full Read):", placeholder="Enter email...")
    phone_input = st.text_input("SMS (Quick Hint):", placeholder="Enter phone #...")
    
    if st.button("Subscribe", key="sub_btn", use_container_width=True):
        if email_input or phone_input:
            try:
                # Insert directly into the Supabase 'subscribers' table
                supabase.table('subscribers').insert({"email": email_input, "phone": phone_input}).execute()
                st.success("You are locked in.")
            except Exception as e:
                st.error("Connection error. Try again.")
        else:
            st.warning("Please enter an email or phone number to get the spark.")
    
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

# --- 7. THE NATIVE NAVIGATION ROW (5 COLUMNS) ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Psychology", type="primary" if st.session_state.current_category == "Psychology" else "secondary", use_container_width=True):
        st.session_state.current_category = "Psychology"
        st.rerun()
with col2:
    if st.button("Human History", type="primary" if st.session_state.current_category == "Human History" else "secondary", use_container_width=True):
        st.session_state.current_category = "Human History"
        st.rerun()
with col3:
    if st.button("Physics", type="primary" if st.session_state.current_category == "Physics" else "secondary", use_container_width=True):
        st.session_state.current_category = "Physics"
        st.rerun()
with col4:
    if st.button("Biology", type="primary" if st.session_state.current_category == "Biology" else "secondary", use_container_width=True):
        st.session_state.current_category = "Biology"
        st.rerun()
with col5:
    if st.button("Technology", type="primary" if st.session_state.current_category == "Technology" else "secondary", use_container_width=True):
        st.session_state.current_category = "Technology"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- 8. FETCH AND RENDER THE LIVE CONTENT ---
vault_data = fetch_daily_shift(st.session_state.current_category)

if vault_data:
    st.markdown(f"<div class='hook-text'>{vault_data['hook']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-text'><div class='section-title'>The Facts</div>{vault_data['mechanism']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-text'><div class='section-title'>So What?</div>{vault_data['shift']}</div>", unsafe_allow_html=True)
    
    # NEW CITATION INJECTION
    if vault_data.get('source_citation'):
        st.markdown(f"<div style='text-align: center; color: #888; font-size: 0.85rem; margin-top: 40px; font-family: monospace;'>Source: {vault_data['source_citation']}</div>", unsafe_allow_html=True)
        
else:
    st.markdown(f"<div class='hook-text'>The engine is currently hunting the archives for {st.session_state.current_category}.</div>", unsafe_allow_html=True)
    st.markdown("<div class='body-text'><div class='section-title'>Status: Pending</div>The AI Editor has not yet published an essay for this discipline. It will wake up tonight at 2:00 AM to scan the global research networks.</div>", unsafe_allow_html=True)
    st.markdown("<div class='body-text'><div class='section-title'>Next Steps</div>Check back tomorrow morning to see what reality it shatters next.</div>", unsafe_allow_html=True)

# Dynamic Sign-off
st.markdown(f"<div class='sign-off'>Think about that. See you tomorrow.</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
