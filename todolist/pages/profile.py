import streamlit as st
import utils.session as sess
import utils.database as dblayer
from utils.helpers import format_date

# UI components
import components.navbar as navbar
import components.footer as footer

def render_profile(user_id):
    """Render the Profile Page."""
    # 1. Load Statistics for User Profile
    all_tasks = dblayer.read_json(dblayer.TASKS_FILE)
    all_history = dblayer.read_json(dblayer.HISTORY_FILE)

    user_tasks = [t for t in all_tasks if t.get("user_id") == user_id]
    user_history = [t for t in all_history if t.get("user_id") == user_id]

    pending_count = len([t for t in user_tasks if t.get("status") == "pending"])
    completed_count = len([t for t in user_tasks if t.get("status") == "completed"])
    deleted_count = len(user_history)
    total_count = pending_count + completed_count + deleted_count

    # 2. Render Navbar
    navbar.render_navbar("My Profile")

    # 3. Main profile sections
    col_card, col_settings = st.columns([0.45, 0.55])

    with col_card:
        st.markdown("<div class='glass-card anim-fade-in' style='text-align: center;'>", unsafe_allow_html=True)
        
        # Generate Profile Avatar Icon
        avatar_letter = st.session_state.username[0].upper() if st.session_state.username else "U"
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">
            <div style="
                width: 100px; 
                height: 100px; 
                border-radius: 50%; 
                background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%); 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                color: white; 
                font-weight: 700; 
                font-size: 2.5rem;
                box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
            ">
                {avatar_letter}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"### {st.session_state.user_name}")
        st.write(f"@{st.session_state.username}")
        st.write(f"📧 `{st.session_state.user_email}`")
        
        created_date = format_date(st.session_state.user_created_at, include_time=False)
        st.markdown(f"""
        <hr style="border: 1px solid var(--border-color); margin: 1rem 0;" />
        <div style="font-size: 0.85rem; color: var(--text-muted);">
            Account created on: <b>{created_date}</b>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_settings:
        # 4. Settings Card (Theme customization)
        st.markdown("<div class='glass-card anim-fade-in'>", unsafe_allow_html=True)
        st.write("### ⚙️ Theme Customization")
        
        theme_choices = ["Dark", "Light"]
        default_theme_index = theme_choices.index(st.session_state.theme) if st.session_state.theme in theme_choices else 0
        
        selected_theme = st.selectbox(
            "Application Theme",
            theme_choices,
            index=default_theme_index,
            help="Select look and feel colors."
        )
        
        if st.button("Apply Theme", type="primary", use_container_width=True):
            # Save to settings.json
            settings = dblayer.read_json(dblayer.SETTINGS_FILE)
            settings[user_id] = {
                "theme": selected_theme
            }
            dblayer.write_json(dblayer.SETTINGS_FILE, settings)
            
            st.session_state.theme = selected_theme
            st.success(f"Applied {selected_theme} mode!")
            sess.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 5. Overall statistics
        st.markdown("<div class='glass-card anim-fade-in'>", unsafe_allow_html=True)
        st.write("### 📈 Lifetime Summary")
        
        st.write(f"📁 **Total Created Tasks:** `{total_count}`")
        st.write(f"✅ **Completed Tasks:** `{completed_count}`")
        st.write(f"⏳ **Pending Tasks:** `{pending_count}`")
        st.write(f"🗑️ **Deleted Tasks:** `{deleted_count}`")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # 6. Footer
    footer.render_footer()
