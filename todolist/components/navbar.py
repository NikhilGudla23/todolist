import streamlit as st
import utils.database as dblayer
from utils.helpers import get_user_level

def render_navbar(page_title):
    """
    Render top navbar, displaying user details and their gamified level badge.
    """
    username = st.session_state.get("username", "User")
    name = st.session_state.get("user_name", username)
    user_id = st.session_state.get("user_id")
    avatar_letter = username[0].upper() if username else "U"
    
    # Calculate current level
    completed_count = 0
    if user_id:
        try:
            all_tasks = dblayer.read_json(dblayer.TASKS_FILE)
            user_tasks = [t for t in all_tasks if t.get("user_id") == user_id]
            completed_count = len([t for t in user_tasks if t.get("status") == "completed"])
        except Exception:
            pass
            
    level_name, level_code = get_user_level(completed_count)
    
    navbar_html = f"""
    <div class="anim-fade-in" style="
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 0.75rem 1.25rem; 
        background: var(--card-bg); 
        border: 1px solid var(--border-color);
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px var(--shadow-color);
    ">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.25rem;">✨</span>
            <span style="font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.25rem; color: var(--text-color); margin: 0;">
                {page_title}
            </span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.15rem;">
                <span style="font-size: 0.875rem; color: var(--text-color); font-weight: 600;">
                    {name}
                </span>
                <span class="level-badge">
                    {level_code} | {level_name}
                </span>
            </div>
            <div style="
                width: 38px; 
                height: 38px; 
                border-radius: 50%; 
                background: linear-gradient(135deg, #00f0ff 0%, #6366f1 100%); 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                color: white; 
                font-weight: 700; 
                font-size: 1rem;
                box-shadow: 0 2px 10px rgba(0, 240, 255, 0.4);
            ">
                {avatar_letter}
            </div>
        </div>
    </div>
    """
    st.markdown(navbar_html, unsafe_allow_html=True)
