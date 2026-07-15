import os
import streamlit as st
from styles.animations import get_animations

def load_theme():
    """Load, build, and inject full CSS style rules depending on current theme selection."""
    theme_choice = st.session_state.get("theme", "Dark")
    
    # 1. Enforce core CSS Variables overrides for Streamlit container containers
    if theme_choice == "Light":
        theme_variables = """
        :root {
            --bg-color: #f3f4f6;
            --card-bg: rgba(255, 255, 255, 0.85);
            --text-color: #1f2937;
            --text-muted: #6b7280;
            --border-color: #e5e7eb;
            --shadow-color: rgba(0, 0, 0, 0.05);
            --primary-color: #3b82f6;
            --accent-color: #6366f1;
        }
        
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #f3f4f6 !important;
            color: #1f2937 !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e5e7eb !important;
        }
        
        /* Change Streamlit default input styles to match Light Mode */
        div[data-baseweb="input"] {
            background-color: #ffffff !important;
            color: #1f2937 !important;
            border: 1px solid #cbd5e1 !important;
        }
        
        div[data-baseweb="select"] {
            background-color: #ffffff !important;
            color: #1f2937 !important;
        }
        
        .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
            color: #1f2937 !important;
        }
        """
    else:
        theme_variables = """
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(26, 32, 53, 0.75);
            --text-color: #f1f5f9;
            --text-muted: #9ca3af;
            --border-color: #2a3447;
            --shadow-color: rgba(0, 0, 0, 0.35);
            --primary-color: #6366f1;
            --accent-color: #a78bfa;
        }
        
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0b0f19 !important;
            color: #f1f5f9 !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid #1f2937 !important;
        }
        
        /* Input overrides for Dark Mode */
        div[data-baseweb="input"] {
            background-color: #1f2937 !important;
            color: #f1f5f9 !important;
            border: 1px solid #374151 !important;
        }
        
        .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
            color: #f1f5f9 !important;
        }
        """
        
    # 2. Read styles/style.css
    css_content = ""
    css_path = os.path.join("styles", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
    # 3. Read animations CSS
    animations_content = get_animations()
    
    # 4. Inject
    combined_css = f"""
    <style>
    {theme_variables}
    {css_content}
    {animations_content}
    </style>
    """
    st.markdown(combined_css, unsafe_allow_html=True)
