import streamlit as st
import utils.session as sess
from styles.theme import load_theme

# Page config (must be the first Streamlit command)
st.set_page_config(
    page_title="TaskFlow Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session
sess.init_session()

# Check Activity Timeout
sess.check_timeout()

# Inject Dynamic CSS and Animations Theme
load_theme()

# Page routing check
if not st.session_state.get("logged_in", False):
    if st.session_state.get("auth_page", "Login") == "Login":
        import pages.login as login_page
        login_page.render_login()
    else:
        import pages.register as register_page
        register_page.render_register()
else:
    # Render Sidebar
    import components.sidebar as sidebar
    sidebar.render_sidebar(st.session_state.get("current_page", "Dashboard"))
    
    current = st.session_state.get("current_page", "Dashboard")
    user_id = st.session_state.user_id
    
    if current == "Dashboard":
        import pages.dashboard as dashboard_page
        dashboard_page.render_dashboard(user_id)
    elif current == "History":
        import pages.history as history_page
        history_page.render_history(user_id)
    elif current == "Profile":
        import pages.profile as profile_page
        profile_page.render_profile(user_id)
