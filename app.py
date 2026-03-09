import streamlit as st
import random
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# --- 1. SETUP ---
load_dotenv()

st.set_page_config(
    page_title="Think With Shane",
    page_icon="⚡",
    layout="centered"
)

# Initialize Supabase
@st.cache_resource
def init_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

supabase = init_supabase()

# --- 2. DATA ---
def fetch_daily_shift(category):
    try:
        response = supabase.table('reality_shifts').select("*").eq('category', category).order('created_at', desc=True).limit(1).execute()
        return response.data[0] if response.data else None
    except: return None

categories = ["Psychology", "Human Systems", "Physics", "Biology"]
if 'current_category' not in st.session_state:
    st.session_state.current_category = random.choice(categories)

themes = {
    "Biology": {"primary": "#7FFFD4", "secondary": "#50C878", "orb": "rgba(127, 255, 212, 0.15)"},
    "Psychology": {"primary": "#B57EDC", "secondary": "#9370DB", "orb": "rgba(181, 126, 220, 0.15)"},
    "Physics": {"primary": "#00FFFF", "secondary": "#4169E1", "orb": "rgba(0, 255, 255, 0.12)"},
    "Human Systems": {"primary": "#FFBF00", "secondary": "#FF4500", "orb": "rgba(255, 191, 0, 0.12)"}
}
active_theme = themes[st.session_state.current_category]

# --- 3. THE ULTIMATE CLEAN CSS ---
st.markdown(f"""
    <style>
    /* Nuke all Streamlit UI */
    [data-testid="stHeader"], [data-testid="stToolbar"], footer, .viewerBadge_container {{ display: none !important; }}
    
    .stApp {{ 
        background: #020403;
        background-attachment: fixed;
    }}
    
    /* Centered Content Wrapper */
    .main-container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
    
    .hook-text {{ color: {active_theme['primary']}; font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 40px; font-family: 'Georgia', serif; }}
    .section-title {{ color: {active_theme['secondary']}; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid {active_theme['orb']}; margin-bottom: 15px; padding-bottom: 5px; }}
    .body-text {{ color: #F0F0F0; font-size: 1.15rem; line-height: 1.8; margin-bottom: 40px; }}
    
    /* Footer Mission Styling */
    .mission-box {{ 
        background: rgba(255,255,255,0.03); 
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid rgba(255,255,255,0.05);
        margin-top: 80px;
        text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. NAVIGATION ---
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)
for i, cat in enumerate(categories):
    with cols[i]:
        if st.button(cat.split()[0], type="primary" if st.session_state.current_category == cat else "secondary", use_container_width=True):
            st.session_state.current_category = cat
            st.rerun()

# --- 5. CONTENT ---
data = fetch_daily_shift(st.session_state.current_category)
if data:
    st.markdown(f"<div class='hook-text'>{data['hook']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>The Mechanism</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-text'>{data['mechanism']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>The Shift</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-text'>{data['shift']}</div>", unsafe_allow_html=True)

# --- 6. THE MISSION (IN-LINE PIVOT) ---
st.markdown(f"""
    <div class='mission-box'>
        <h3 style='color: {active_theme['primary']};'>The Mission</h3>
        <p style='color: #A0A0A0; font-size: 0.95rem;'>
            This space is designed to make you think. We translate academic research into daily reality shifts 
            to help you discover what you were never taught and question the systems you blindly accept.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
with st.container():
    st.markdown("<h4 style='text-align: center; color: white;'>Get the Spark</h4>", unsafe_allow_html=True)
    email = st.text_input("Email", label_visibility="collapsed", placeholder="Your email...")
    if st.button("Subscribe", use_container_width=True, type="primary"):
        st.success("You're in.")

st.markdown(f"<div style='text-align: center; margin-top: 50px; opacity: 0.3; font-size: 0.8rem; color: white;'>THINKWITHSHANE</div>", unsafe_allow_html=True)
