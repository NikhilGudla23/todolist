def search_tasks(tasks, query):
    """
    Search list of tasks by checking if query string is a substring in task properties.
    Case-insensitive search.
    """
    if not query or not query.strip():
        return tasks
        
    query_clean = query.strip().lower()
    results = []
    
    for task in tasks:
        title = task.get("title", "").lower()
        description = task.get("description", "").lower() if task.get("description") else ""
        category = task.get("category", "").lower()
        priority = task.get("priority", "").lower()
        status = task.get("status", "").lower()
        
        if (query_clean in title or 
            query_clean in description or 
            query_clean in category or 
            query_clean in priority or 
            query_clean in status):
            results.append(task)
            
    return results
