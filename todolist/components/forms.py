from datetime import datetime
import streamlit as st
import utils.database as db
import utils.validation as val
import utils.logger as log
import utils.session as sess
from utils.constants import PRIORITIES, CATEGORIES

def render_add_task_form(user_id):
    """
    Render form for creating a new task, featuring real-time AI auto-suggestions.
    """
    st.markdown("<div class='glass-card anim-fade-in'>", unsafe_allow_html=True)
    st.write("### ➕ Create Task")
    
    # We do NOT use st.form here to enable interactive real-time AI suggestions
    title = st.text_input("Task Title *", placeholder="E.g., Prepare board presentation or Buy milk...", key="add_title").strip()
    
    # Run Heuristic AI recommendations
    s_cat, s_pri = None, None
    if title:
        from utils.ai import suggest_task_meta
        s_cat, s_pri = suggest_task_meta(title)
        if s_cat:
            st.markdown(f"""
            <div style="
                background-color: rgba(0, 240, 255, 0.08); 
                border-left: 3px solid #00f0ff; 
                padding: 0.6rem 0.8rem; 
                border-radius: 8px; 
                font-size: 0.825rem; 
                margin-bottom: 1rem; 
                color: #00f0ff; 
                font-weight: 500;
                box-shadow: 0 0 10px rgba(0, 240, 255, 0.1);
            ">
                🤖 <b>AI Metadata Recommendation:</b> Set Category to <b>{s_cat}</b> | Recommended Priority: <b>{s_pri}</b>
            </div>
            """, unsafe_allow_html=True)
            
    description = st.text_area("Description (Optional)", placeholder="Add details...").strip()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        default_cat_index = CATEGORIES.index(s_cat) if s_cat in CATEGORIES else 0
        category = st.selectbox("Category", CATEGORIES, index=default_cat_index, key="add_category")
    with col2:
        default_pri_index = PRIORITIES.index(s_pri) if s_pri in PRIORITIES else 1
        priority = st.selectbox("Priority", PRIORITIES, index=default_pri_index, key="add_priority")
    with col3:
        due_date = st.date_input("Due Date", min_value=datetime.today(), key="add_due_date")
    with col4:
        duration = st.number_input("Duration (m)", min_value=0, value=0, step=5, key="add_duration")
        
    submit = st.button("➕ Add Task", type="primary", use_container_width=True)
    
    if submit:
        # Validate inputs
        if not val.validate_task_title(title):
            st.error("Task title must be non-empty and under 100 characters.")
        elif not val.validate_task_description(description):
            st.error("Description must be under 500 characters.")
        else:
            try:
                tasks = db.read_json(db.TASKS_FILE)
                
                new_task = {
                    "id": str(datetime.now().timestamp()),
                    "user_id": user_id,
                    "title": title,
                    "description": description if description else None,
                    "priority": priority,
                    "category": category,
                    "status": "pending",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "due_date": due_date.strftime("%Y-%m-%d"),
                    "duration": int(duration)
                }
                
                tasks.append(new_task)
                db.write_json(db.TASKS_FILE, tasks)
                st.success(f"Added task: '{title}'")
                log.info(f"User {user_id} created task: {title}")
                sess.rerun()
            except Exception as e:
                st.error(f"Failed to add task: {e}")
                log.error(f"Error adding task: {e}")
                
    st.markdown("</div>", unsafe_allow_html=True)

def render_edit_task_form(user_id, task_id):
    """
    Render edit form inline.
    """
    st.markdown("<div class='glass-card anim-card-pop'>", unsafe_allow_html=True)
    st.write("### ✏️ Edit Task")
    
    # Fetch task detail
    tasks = db.read_json(db.TASKS_FILE)
    task_to_edit = None
    for task in tasks:
        if task["id"] == task_id and task["user_id"] == user_id:
            task_to_edit = task
            break
            
    if not task_to_edit:
        st.error("Task not found!")
        st.markdown("</div>", unsafe_allow_html=True)
        return
        
    try:
        due_date_default = datetime.strptime(task_to_edit["due_date"], "%Y-%m-%d").date()
    except Exception:
        due_date_default = datetime.today().date()
        
    with st.form("edit_task_form"):
        title = st.text_input("Task Title *", value=task_to_edit["title"]).strip()
        description = st.text_area("Description (Optional)", value=task_to_edit.get("description", "") or "").strip()
        
        default_duration = int(task_to_edit.get("duration", 0))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            cat_index = CATEGORIES.index(task_to_edit["category"]) if task_to_edit["category"] in CATEGORIES else 0
            category = st.selectbox("Category", CATEGORIES, index=cat_index)
        with col2:
            pri_index = PRIORITIES.index(task_to_edit["priority"]) if task_to_edit["priority"] in PRIORITIES else 1
            priority = st.selectbox("Priority", PRIORITIES, index=pri_index)
        with col3:
            due_date = st.date_input("Due Date", value=due_date_default)
        with col4:
            duration = st.number_input("Duration (m)", min_value=0, value=default_duration, step=5)
            
        col_btn1, col_btn2 = st.columns([0.8, 0.2])
        with col_btn1:
            save = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
        with col_btn2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
            
        if save:
            if not val.validate_task_title(title):
                st.error("Task title must be non-empty and under 100 characters.")
            elif not val.validate_task_description(description):
                st.error("Description must be under 500 characters.")
            else:
                # Update task
                for task in tasks:
                    if task["id"] == task_id:
                        task["title"] = title
                        task["description"] = description if description else None
                        task["category"] = category
                        task["priority"] = priority
                        task["due_date"] = due_date.strftime("%Y-%m-%d")
                        task["duration"] = int(duration)
                        task["updated_at"] = datetime.now().isoformat()
                        break
                db.write_json(db.TASKS_FILE, tasks)
                st.session_state.edit_todo_id = None
                log.info(f"User {user_id} updated task: {task_id}")
                st.success("Task updated!")
                sess.rerun()
                
        if cancel:
            st.session_state.edit_todo_id = None
            sess.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
