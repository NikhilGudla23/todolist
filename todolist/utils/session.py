import time
import streamlit as st

# Session timeout limit in seconds (30 minutes)
TIMEOUT_LIMIT = 1800

def rerun():
    """Rerun the Streamlit script, compatible with older versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def init_session():
    """Initialize all session state variables if not already set."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "Login"
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_created_at" not in st.session_state:
        st.session_state.user_created_at = None
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"
        
    # Edit Task buffer
    if "edit_todo_id" not in st.session_state:
        st.session_state.edit_todo_id = None
        
    # Confirmation triggers
    if "delete_confirm_id" not in st.session_state:
        st.session_state.delete_confirm_id = None
    if "confirm_clear_all" not in st.session_state:
        st.session_state.confirm_clear_all = False
        
    # Activity tracking for session timeout
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = time.time()
        
    # Pomodoro session state
    if "pomodoro_active" not in st.session_state:
        st.session_state.pomodoro_active = False
    if "pomodoro_start_time" not in st.session_state:
        st.session_state.pomodoro_start_time = None
    if "pomodoro_duration" not in st.session_state:
        st.session_state.pomodoro_duration = 1500
    if "pomodoro_task_id" not in st.session_state:
        st.session_state.pomodoro_task_id = None

def update_activity():
    """Update last activity timestamp to prevent session timeout."""
    st.session_state.last_activity = time.time()

def check_timeout():
    """Check if the user has been inactive for longer than TIMEOUT_LIMIT."""
    if st.session_state.get("logged_in", False):
        current_time = time.time()
        elapsed = current_time - st.session_state.get("last_activity", current_time)
        
        if elapsed > TIMEOUT_LIMIT:
            # Session expired
            logout()
            st.warning("⏱️ Session expired due to inactivity. Please log in again.")
            rerun()
            st.stop()
        else:
            update_activity()

def login(user_record):
    """Set session state variables on successful login."""
    st.session_state.logged_in = True
    st.session_state.user_id = user_record["id"]
    st.session_state.username = user_record["username"]
    st.session_state.user_name = user_record.get("name", user_record["username"])
    st.session_state.user_email = user_record.get("email", "")
    st.session_state.user_created_at = user_record.get("created_at", "")
    st.session_state.last_activity = time.time()
    st.session_state.current_page = "Dashboard"
    
    # Load user's theme settings from settings.json if available
    from utils.database import read_json, SETTINGS_FILE
    settings = read_json(SETTINGS_FILE)
    user_settings = settings.get(user_record["id"], {})
    st.session_state.theme = user_settings.get("theme", "Dark")

def logout():
    """Clear all session states and reset to default."""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.session_state.user_created_at = None
    st.session_state.edit_todo_id = None
    st.session_state.delete_confirm_id = None
    st.session_state.confirm_clear_all = False
    st.session_state.auth_page = "Login"
    st.session_state.current_page = "Dashboard"
    st.session_state.pomodoro_active = False
    st.session_state.pomodoro_start_time = None
    st.session_state.pomodoro_duration = 1500
    st.session_state.pomodoro_task_id = None
    st.session_state.last_activity = time.time()
