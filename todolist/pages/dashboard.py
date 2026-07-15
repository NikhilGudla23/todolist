import time
import streamlit as st
import utils.session as sess
import utils.database as dblayer
import utils.search as searcher
import utils.filter as filterer
import utils.sort as sorter

# UI components
import components.navbar as navbar
import components.cards as cards
import components.forms as forms
import components.tables as tables
import components.statistics as stats
import components.footer as footer

def render_dashboard(user_id):
    """Render the divided Dashboard Page."""
    # 1. Load User Data
    all_tasks = dblayer.read_json(dblayer.TASKS_FILE)
    all_history = dblayer.read_json(dblayer.HISTORY_FILE)

    user_tasks = [t for t in all_tasks if t.get("user_id") == user_id]
    user_history = [t for t in all_history if t.get("user_id") == user_id]

    active_tasks = [t for t in user_tasks if t.get("status") == "pending"]
    completed_tasks = [t for t in user_tasks if t.get("status") == "completed"]

    pending_count = len(active_tasks)
    completed_count = len(completed_tasks)
    deleted_count = len(user_history)
    total_active = pending_count + completed_count
    
    # Calculate Backlog Workload in minutes
    backlog_minutes = sum(int(t.get("duration", 0)) for t in active_tasks)
    completion_rate = (completed_count / total_active * 100) if total_active > 0 else 0.0

    # 2. Render Navbar
    navbar.render_navbar("Dashboard Overview")

    # 3. Stats widgets (workload backlog replaces total created count)
    cards.render_stats_cards(backlog_minutes, completed_count, pending_count, deleted_count, completion_rate)

    # 4. Tab Division
    tab_board, tab_analytics, tab_focus = st.tabs(["📋 Task Board", "📊 Productivity Analytics", "⏱️ Focus Space"])

    with tab_board:
        # Edit Task overlays Add Task Form if edit is active
        edit_id = st.session_state.get("edit_todo_id")
        if edit_id:
            forms.render_edit_task_form(user_id, edit_id)
        else:
            forms.render_add_task_form(user_id)

        st.markdown("<hr style='border: 1px solid var(--border-color); margin: 2rem 0;' />", unsafe_allow_html=True)

        # Search, Filter, Sort Controls
        st.markdown("<div class='glass-card anim-fade-in'>", unsafe_allow_html=True)
        st.write("### 🔍 Search, Filter & Sort Tasks")

        col_search, col_sort = st.columns([0.65, 0.35])
        with col_search:
            search_query = st.text_input("Search tasks...", placeholder="Type task details...").strip()

        with col_sort:
            sort_choice = st.selectbox("Sort By", ["Newest", "Oldest", "Priority", "Alphabetical", "Due Date", "Status"], index=0)

        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            status_filter = st.selectbox("Filter Status", ["All", "Pending", "Completed"], index=0)
        with col_f2:
            priority_filter = st.selectbox("Filter Priority", ["All", "High", "Medium", "Low"], index=0)
        with col_f3:
            from utils.constants import CATEGORIES
            category_filter = st.selectbox("Filter Category", ["All"] + CATEGORIES, index=0)
        with col_f4:
            date_filter = st.selectbox("Filter Due Date", ["All", "Today", "This Week"], index=0)

        st.markdown("</div>", unsafe_allow_html=True)

        # Apply Search, Filter, Sort Algorithms
        filtered_tasks = filterer.filter_tasks(
            user_tasks, 
            status=status_filter, 
            priority=priority_filter, 
            category=category_filter, 
            time_frame=date_filter
        )
        searched_tasks = searcher.search_tasks(filtered_tasks, search_query)
        sorted_tasks = sorter.sort_tasks(searched_tasks, sort_choice)

        st.write("### 📋 Active Task List")
        tables.render_task_table(user_id, sorted_tasks)

    with tab_analytics:
        # Render Charts Analytics Panel
        stats.render_task_charts(active_tasks, completed_tasks, user_history)

    with tab_focus:
        st.write("### ⏱️ Focus Space")
        st.write("Select a task from your backlog and start a ticking Pomodoro focus session to boost your workflow.")
        
        pending_task_titles = [t["title"] for t in active_tasks]
        if not pending_task_titles:
            st.info("No active tasks available to focus on. Add a task in the Task Board first!")
        else:
            task_selected = st.selectbox("Select a task to focus on", pending_task_titles)
            
            # Select session duration
            session_type = st.radio("Select Session Type", ["Focus Session (25m)", "Short Break (5m)", "Long Break (15m)"], index=0, horizontal=True)
            
            duration_map = {
                "Focus Session (25m)": 1500,
                "Short Break (5m)": 300,
                "Long Break (15m)": 900
            }
            selected_duration = duration_map[session_type]
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if not st.session_state.get("pomodoro_active", False):
                    if st.button("🚀 Start Focus Session", type="primary", use_container_width=True):
                        st.session_state.pomodoro_active = True
                        st.session_state.pomodoro_start_time = time.time()
                        st.session_state.pomodoro_duration = selected_duration
                        st.session_state.pomodoro_task_title = task_selected
                        sess.rerun()
                else:
                    if st.button("🛑 Cancel Session", type="secondary", use_container_width=True):
                        st.session_state.pomodoro_active = False
                        st.session_state.pomodoro_start_time = None
                        st.session_state.pomodoro_task_title = None
                        sess.rerun()
            
            # Run Pomodoro Ticking Timer
            if st.session_state.get("pomodoro_active", False):
                has_autorefresh = False
                try:
                    from streamlit_autorefresh import st_autorefresh  # type: ignore
                    has_autorefresh = True
                except ImportError:
                    pass
                
                if has_autorefresh:
                    # Auto-refresh script every 1 second when focus timer is active
                    st_autorefresh(interval=1000, limit=10000, key="pomodoro_tick")
                else:
                    st.warning("Auto-refresh module not available. Click 'Sync Timer' below to tick down.")
                    if st.button("🔄 Sync Timer Status", use_container_width=True):
                        sess.rerun()
                
                elapsed = time.time() - st.session_state.pomodoro_start_time
                remaining = max(0, st.session_state.pomodoro_duration - elapsed)
                
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                time_str = f"{mins:02d}:{secs:02d}"
                
                # Visual Timer Card
                st.markdown(f"""
                <div class="glass-card" style="
                    text-align: center; 
                    border: 1px solid var(--primary-color); 
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.25); 
                    margin-top: 1.5rem; 
                    padding: 2.5rem;
                ">
                    <h4 style="color: var(--text-color); margin-bottom: 0.5rem; font-family: 'Poppins', sans-serif;">Focusing on: <b>{st.session_state.pomodoro_task_title}</b></h4>
                    <div style="font-size: 5rem; font-weight: 700; font-family: 'Poppins', sans-serif; color: var(--accent-color); letter-spacing: 0.05em; margin: 1rem 0; text-shadow: 0 0 10px rgba(167, 139, 250, 0.4);">
                        {time_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Ticking Progress Bar
                progress_val = min(1.0, elapsed / st.session_state.pomodoro_duration)
                st.progress(progress_val)
                
                # Completion check
                if remaining == 0:
                    st.session_state.pomodoro_active = False
                    st.session_state.pomodoro_start_time = None
                    st.session_state.pomodoro_task_title = None
                    st.balloons()
                    st.success("🎉 Focus session completed! Excellent work!")
                    from utils.logger import info
                    info(f"User completed focus session for: {task_selected}")
                    sess.rerun()
            else:
                st.markdown("""
                <div class="glass-card" style="text-align: center; margin-top: 1.5rem; padding: 2rem;">
                    <p style="color: var(--text-muted); font-size: 0.95rem;">Focus Timer is not active. Click the button above to start your session.</p>
                </div>
                """, unsafe_allow_html=True)

    # 5. Footer
    footer.render_footer()
