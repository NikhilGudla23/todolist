def sort_tasks(tasks, sort_by):
    """
    Sort tasks based on user choice: Newest, Oldest, Priority, Alphabetical, Due Date, Status.
    """
    if not tasks:
        return tasks
        
    if sort_by == "Newest":
        return sorted(tasks, key=lambda x: x.get("created_at", ""), reverse=True)
        
    elif sort_by == "Oldest":
        return sorted(tasks, key=lambda x: x.get("created_at", ""))
        
    elif sort_by == "Priority":
        # Sort High -> Medium -> Low
        priority_weights = {"High": 3, "Medium": 2, "Low": 1}
        return sorted(tasks, key=lambda x: priority_weights.get(x.get("priority", "Medium"), 2), reverse=True)
        
    elif sort_by == "Alphabetical":
        return sorted(tasks, key=lambda x: x.get("title", "").lower())
        
    elif sort_by == "Due Date":
        # Push empty/null due dates to the very end
        return sorted(tasks, key=lambda x: x.get("due_date") or "9999-12-31")
        
    elif sort_by == "Status":
        # Show pending tasks before completed tasks
        status_order = {"pending": 0, "completed": 1}
        return sorted(tasks, key=lambda x: status_order.get(x.get("status", "pending"), 0))
        
    return tasks
