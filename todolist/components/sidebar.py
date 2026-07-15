import streamlit as st
from streamlit_option_menu import option_menu
import utils.session as sess

def render_sidebar(active_page):
    """
    Render custom sidebar with SaaS branding, option menu navigation, and a logout button.
    """
    with st.sidebar:
        # App branding
        st.markdown("""
        <div class="sidebar-logo" style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
            <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-weight: 700; background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">⚡ TaskFlow Pro</h2>
            <span style="font-size: 0.7rem; color: var(--text-muted); font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase;">Smart Todo SaaS</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar Option Menu
        options = ["Dashboard", "History", "Profile"]
        icons = ["grid", "clock-history", "person"]
        
        try:
            default_index = options.index(active_page)
        except ValueError:
            default_index = 0
            
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            default_index=default_index,
            styles={
                "container": {"background-color": "transparent", "padding": "0px"},
                "icon": {"color": "var(--accent-color)", "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px", 
                    "text-align": "left", 
                    "margin": "4px 0px", 
                    "color": "var(--text-color)",
                    "--hover-color": "rgba(99, 102, 241, 0.1)",
                    "border-radius": "8px"
                },
                "nav-link-selected": {
                    "background-color": "var(--primary-color)", 
                    "color": "white", 
                    "font-weight": "600",
                    "box-shadow": "0 4px 10px rgba(99, 102, 241, 0.25)"
                }
            }
        )
        
        # Switch pages if the selected one is different
        if selected != active_page:
            st.session_state.current_page = selected
            sess.rerun()
                
        # Vertical spacer
        st.markdown("<div style='height: 180px;'></div>", unsafe_allow_html=True)
        
        # Logout button
        st.markdown("<hr style='border: 1px solid var(--border-color); margin-bottom: 1.5rem;' />", unsafe_allow_html=True)
        if st.button("🚪 Log Out", use_container_width=True, type="secondary"):
            sess.logout()
            st.success("Successfully logged out!")
            sess.rerun()
