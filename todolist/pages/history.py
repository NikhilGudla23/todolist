import streamlit as st
from datetime import datetime
import utils.session as sess
import utils.database as dblayer
import utils.search as searcher
import utils.filter as filterer
from utils.helpers import format_date, get_category_icon

# UI components
import components.navbar as navbar
import components.modals as modals
import components.footer as footer

def render_history(user_id):
    """Render the History Page."""
    # 1. Load History Data
    all_history = dblayer.read_json(dblayer.HISTORY_FILE)
    user_history = [h for h in all_history if h.get("user_id") == user_id]

    # 2. Render Navbar
    navbar.render_navbar("Deleted Tasks History")

    # 3. Statistics summary count & Clear all actions
    col_info, col_action = st.columns([0.65, 0.35])
    with col_info:
        st.write(f"You have **{len(user_history)}** deleted items in history.")
        
    with col_action:
        if user_history:
            if not st.session_state.confirm_clear_all:
                if st.button("🗑️ Delete All History", key="btn_clear_all_trigger", type="secondary", use_container_width=True):
                    st.session_state.confirm_clear_all = True
                    sess.rerun()
            else:
                # Render confirmation warning block
                def perform_clear_all():
                    hist = dblayer.read_json(dblayer.HISTORY_FILE)
                    # Keep history of OTHER users, clear for current user
                    updated_hist = [h for h in hist if h.get("user_id") != user_id]
                    dblayer.write_json(dblayer.HISTORY_FILE, updated_hist)
                    st.session_state.confirm_clear_all = False
                    st.success("History cleared completely!")
                    sess.rerun()
                    
                modals.render_confirm_dialog(
                    "Are you sure you want to permanently empty all task history? This is unrecoverable.",
                    "clear_all",
                    perform_clear_all
                )

    st.markdown("<hr style='border: 1px solid var(--border-color); margin-bottom: 2rem;' />", unsafe_allow_html=True)

    # 4. Search and filters on history
    st.markdown("<div class='glass-card anim-fade-in'>", unsafe_allow_html=True)
    st.write("### 🔍 Search History")

    col_search_h, col_f_p, col_f_c = st.columns([0.5, 0.25, 0.25])
    with col_search_h:
        search_query = st.text_input("Search deleted tasks...", placeholder="Search word...").strip()
    with col_f_p:
        pri_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"], key="hist_pri_fil")
    with col_f_c:
        from utils.constants import CATEGORIES
        cat_filter = st.selectbox("Category", ["All"] + CATEGORIES, key="hist_cat_fil")

    st.markdown("</div>", unsafe_allow_html=True)

    # Apply filter & search
    filtered_history = filterer.filter_tasks(user_history, priority=pri_filter, category=cat_filter)
    searched_history = searcher.search_tasks(filtered_history, search_query)

    # Sort history newest deleted first
    sorted_history = sorted(searched_history, key=lambda x: x.get("deleted_at", ""), reverse=True)

    # 5. Deleted Tasks list
    if not sorted_history:
        st.markdown("""
        <div class="empty-state-card">
            <h4>History is empty</h4>
            <p>No deleted items match your search parameters.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for item in sorted_history:
            item_id = item["id"]
            cat_icon = get_category_icon(item["category"])
            del_date = format_date(item.get("deleted_at"))
            
            st.markdown(f"<div class='glass-card anim-fade-in' style='padding: 1rem; border-left: 5px solid #6b7280;'>", unsafe_allow_html=True)
            
            col_text, col_date_deleted, col_restore, col_del_perm = st.columns([0.45, 0.23, 0.15, 0.17])
            
            with col_text:
                st.markdown(f"""
                <div>
                    <span style="font-weight: 600; font-size: 1.05rem; opacity: 0.85;">{item['title']}</span>
                    <div style="margin-top: 0.25rem;">
                        <span class="badge badge-category">{cat_icon} {item['category']}</span>
                        <span class="badge" style="background-color: rgba(107, 114, 128, 0.15); color: #9ca3af;">{item['priority']}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">{item.get('description', '') or ''}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_date_deleted:
                st.markdown(f"""
                <div style="font-size: 0.85rem; color: var(--text-muted);">
                    🗑️ Deleted on:<br/><b>{del_date}</b>
                </div>
                """, unsafe_allow_html=True)
                
            with col_restore:
                if st.button("↩️ Restore", key=f"restore_{item_id}", use_container_width=True):
                    try:
                        hist = dblayer.read_json(dblayer.HISTORY_FILE)
                        tasks = dblayer.read_json(dblayer.TASKS_FILE)
                        
                        # Remove from history
                        hist_updated = [h for h in hist if h["id"] != item_id]
                        dblayer.write_json(dblayer.HISTORY_FILE, hist_updated)
                        
                        # Restore back to tasks list as pending
                        restored_task = {
                            "id": item["id"],
                            "user_id": user_id,
                            "title": item["title"],
                            "description": item.get("description"),
                            "priority": item["priority"],
                            "category": item["category"],
                            "status": "pending",
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat(),
                            "due_date": datetime.now().strftime("%Y-%m-%d") # default back to today
                        }
                        tasks.append(restored_task)
                        dblayer.write_json(dblayer.TASKS_FILE, tasks)
                        
                        st.success("Task restored to dashboard!")
                        sess.rerun()
                    except Exception as e:
                        st.error(f"Failed to restore task: {e}")
                        
            with col_del_perm:
                if st.session_state.delete_confirm_id != item_id:
                    if st.button("🗑️ Delete Perm", key=f"del_perm_req_{item_id}", use_container_width=True):
                        st.session_state.delete_confirm_id = item_id
                        sess.rerun()
                else:
                    # Render permanent delete verification dialog
                    def perform_delete_perm():
                        hist = dblayer.read_json(dblayer.HISTORY_FILE)
                        updated_hist = [h for h in hist if h["id"] != item_id]
                        dblayer.write_json(dblayer.HISTORY_FILE, updated_hist)
                        st.session_state.delete_confirm_id = None
                        st.success("Permanently removed from database.")
                        sess.rerun()
                        
                    modals.render_confirm_dialog(
                        "Permanently delete this task? This is unrecoverable.",
                        f"del_{item_id}",
                        perform_delete_perm
                    )
                    
            st.markdown("</div>", unsafe_allow_html=True)

    # 6. Footer
    footer.render_footer()
