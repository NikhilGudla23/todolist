import streamlit as st
import pandas as pd
import plotly.express as px

def render_task_charts(active_tasks, completed_tasks, deleted_tasks):
    """
    Render analytical dashboards of user's task database records using Plotly.
    """
    total_active_count = len(active_tasks)
    total_completed_count = len(completed_tasks)
    total_deleted_count = len(deleted_tasks)
    
    st.write("### 📊 Task Analytics")
    
    # Empty statistics check
    if total_active_count == 0 and total_completed_count == 0 and total_deleted_count == 0:
        st.info("No data available to display statistics. Create some tasks first!")
        return
        
    col_chart1, col_chart2 = st.columns(2)
    
    # Prepare task datasets
    all_active_completed = active_tasks + completed_tasks
    
    # 1. Category Distribution Donut Chart
    with col_chart1:
        if all_active_completed:
            df = pd.DataFrame(all_active_completed)
            # Count values per category
            cat_counts = df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            
            fig_cat = px.pie(
                cat_counts, 
                values="Count", 
                names="Category", 
                hole=0.4,
                title="Tasks by Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="var(--text-color)",
                margin=dict(t=40, b=10, l=10, r=10),
                height=280
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No active or completed tasks to show category breakdown.")
            
    # 2. Priority Distribution Pie Chart
    with col_chart2:
        if all_active_completed:
            df = pd.DataFrame(all_active_completed)
            pri_counts = df["priority"].value_counts().reset_index()
            pri_counts.columns = ["Priority", "Count"]
            
            # Map colors to match the SaaS palette (Red, Amber, Emerald)
            priority_color_map = {
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Low": "#10b981"
            }
            
            fig_pri = px.pie(
                pri_counts,
                values="Count",
                names="Priority",
                title="Tasks by Priority",
                color="Priority",
                color_discrete_map=priority_color_map
            )
            fig_pri.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="var(--text-color)",
                margin=dict(t=40, b=10, l=10, r=10),
                height=280
            )
            st.plotly_chart(fig_pri, use_container_width=True)
        else:
            st.info("No active or completed tasks to show priority levels.")
