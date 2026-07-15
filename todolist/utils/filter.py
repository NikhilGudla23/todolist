from datetime import datetime, timedelta

def filter_tasks(tasks, status="All", priority="All", category="All", time_frame="All"):
    """
    Filter tasks list based on status, priority, category, and due date range.
    """
    filtered = tasks
    
    # 1. Filter by Status
    if status != "All":
        filtered = [t for t in filtered if t.get("status") == status.lower()]
        
    # 2. Filter by Priority
    if priority != "All":
        filtered = [t for t in filtered if t.get("priority") == priority]
        
    # 3. Filter by Category
    if category != "All":
        filtered = [t for t in filtered if t.get("category") == category]
        
    # 4. Filter by Date range (Today / This Week)
    if time_frame != "All":
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        if time_frame == "Today":
            filtered = [t for t in filtered if t.get("due_date") == today_str]
            
        elif time_frame == "This Week":
            today = datetime.now().date()
            end_week = today + timedelta(days=6)
            
            weekly_tasks = []
            for t in filtered:
                due_str = t.get("due_date")
                if due_str:
                    try:
                        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
                        if today <= due_date <= end_week:
                            weekly_tasks.append(t)
                    except Exception:
                        pass
            filtered = weekly_tasks
            
    return filtered
