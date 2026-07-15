from datetime import datetime
import streamlit as st
import utils.database as db
import utils.logger as log
import utils.session as sess
from utils.helpers import format_date, get_category_icon, truncate_text, get_relative_due_date
from utils.constants import PRIORITY_BADGES, PRIORITY_COLORS

def render_task_table(user_id, tasks_list):
    """
    Render active todo task table inside columns layout.
    """
    if not tasks_list:
        st.markdown("""
        <div class="empty-state-card">
            <h4>No tasks found</h4>
            <p>Modify search/filters or click above to create a new task.</p>
        </div>
        """, unsafe_allow_html=True)
        return
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    for task in tasks_list:
        task_id = task["id"]
        is_completed = task["status"] == "completed"
        due_date = task.get("due_date", "")
        
        # Check if overdue (pending and due date < today)
        is_overdue = False
        if not is_completed and due_date:
            try:
                is_overdue = due_date < today_str
            except Exception:
                pass
                
        # CSS styling hooks
        priority_border = f"priority-{task['priority'].lower()}-border"
        overdue_class = "anim-pulse-red" if is_overdue else ""
        title_style = "text-decoration: line-through; opacity: 0.5;" if is_completed else ""
        
        # Render row
        st.markdown(f"<div class='glass-card {priority_border} {overdue_class} anim-fade-in' style='margin-bottom: 0.75rem; padding: 1rem;'>", unsafe_allow_html=True)
        
        col_select, col_info, col_date, col_actions = st.columns([0.08, 0.47, 0.22, 0.23])
        
        with col_select:
            # Checkbox to complete/restore task
            check_key = f"chk_{task_id}"
            default_val = is_completed
            checked = st.checkbox("", value=default_val, key=check_key)
            
            if checked != default_val:
                # Update status
                all_tasks = db.read_json(db.TASKS_FILE)
                for t in all_tasks:
                    if t["id"] == task_id:
                        t["status"] = "completed" if checked else "pending"
                        t["updated_at"] = datetime.now().isoformat()
                        break
                db.write_json(db.TASKS_FILE, all_tasks)
                log.info(f"User {user_id} toggled status of task {task_id} to {t['status']}")
                sess.rerun()
                
        with col_info:
            cat_icon = get_category_icon(task["category"])
            desc_text = f"<div style='font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;'>{task['description']}</div>" if task.get("description") else ""
            
            # Badge styles
            badge_pri = PRIORITY_BADGES.get(task["priority"], "badge-medium")
            
            duration_badge = ""
            duration_val = task.get("duration", 0)
            if duration_val > 0:
                duration_badge = f'<span class="badge" style="background-color: rgba(0, 240, 255, 0.1); color: #00f0ff; border-color: rgba(0, 240, 255, 0.25);">⏱️ {duration_val}m</span>'
            
            st.markdown(f"""
            <div style="{title_style}">
                <span style="font-weight: 600; font-size: 1.05rem;">{task['title']}</span>
                <div style="margin-top: 0.35rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="badge badge-category">{cat_icon} {task['category']}</span>
                    <span class="badge {badge_pri}">{task['priority']} Priority</span>
                    {duration_badge}
                </div>
                {desc_text}
            </div>
            """, unsafe_allow_html=True)
            
        with col_date:
            date_icon = "📅" if not is_overdue else "🚨"
            relative_due = get_relative_due_date(due_date)
            st.markdown(f"""
            <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-color);">
                {date_icon} {relative_due}
            </div>
            """, unsafe_allow_html=True)
            
        with col_actions:
            st.markdown("<div style='display: flex; gap: 0.5rem; justify-content: flex-end;'>", unsafe_allow_html=True)
            col_e, col_d = st.columns(2)
            with col_e:
                if st.button("✏️ Edit", key=f"btn_edit_{task_id}", use_container_width=True):
                    st.session_state.edit_todo_id = task_id
                    sess.rerun()
            with col_d:
                # Soft delete: move to history.json
                if st.button("🗑️ Delete", key=f"btn_del_{task_id}", use_container_width=True):
                    try:
                        all_tasks = db.read_json(db.TASKS_FILE)
                        history = db.read_json(db.HISTORY_FILE)
                        
                        # Find task and pop it
                        deleted_task = None
                        remaining_tasks = []
                        for t in all_tasks:
                            if t["id"] == task_id:
                                deleted_task = t
                            else:
                                remaining_tasks.append(t)
                                
                        if deleted_task:
                            db.write_json(db.TASKS_FILE, remaining_tasks)
                            
                            # Add to history
                            history_item = {
                                "id": deleted_task["id"],
                                "user_id": user_id,
                                "title": deleted_task["title"],
                                "description": deleted_task.get("description"),
                                "priority": deleted_task["priority"],
                                "category": deleted_task["category"],
                                "deleted_at": datetime.now().isoformat()
                            }
                            history.append(history_item)
                            db.write_json(db.HISTORY_FILE, history)
                            
                            log.info(f"User {user_id} deleted task: {deleted_task['title']} (moved to history)")
                            st.success("Task deleted (moved to History)")
                            sess.rerun()
                    except Exception as e:
                        st.error(f"Error deleting task: {e}")
                        log.error(f"Error soft deleting task: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
