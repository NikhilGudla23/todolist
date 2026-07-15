import streamlit as st

def render_stats_cards(backlog_minutes, completed, pending, deleted, completion_rate):
    """
    Render statistics metric cards in a grid, including the new Backlog Workload.
    """
    # Format workload duration
    if backlog_minutes >= 60:
        workload_str = f"{backlog_minutes / 60:.1f} hrs"
    else:
        workload_str = f"{backlog_minutes} mins"
        
    cards_html = f"""
    <div class="stat-card-grid anim-fade-in">
        <div class="stat-widget total hover-lift">
            <span class="stat-widget-label">⏱️ Backlog Workload</span>
            <span class="stat-widget-num">{workload_str}</span>
        </div>
        <div class="stat-widget completed hover-lift">
            <span class="stat-widget-label">✅ Completed</span>
            <span class="stat-widget-num">{completed}</span>
        </div>
        <div class="stat-widget pending hover-lift">
            <span class="stat-widget-label">⏳ Pending</span>
            <span class="stat-widget-num">{pending}</span>
        </div>
        <div class="stat-widget deleted hover-lift">
            <span class="stat-widget-label">🗑️ Deleted</span>
            <span class="stat-widget-num">{deleted}</span>
        </div>
        <div class="stat-widget pct hover-lift">
            <span class="stat-widget-label">📈 Completion</span>
            <span class="stat-widget-num">{completion_rate:.1f}%</span>
        </div>
    </div>
    """
    st.markdown(cards_html, unsafe_allow_html=True)
