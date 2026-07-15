# Heuristic AI Auto-Suggestion Engine for TaskFlow Pro

def suggest_task_meta(title):
    """
    Analyze the task title and return suggested (category, priority).
    """
    if not title or not title.strip():
        return None, None
        
    title_lower = title.strip().lower()
    
    # 1. Category heuristics
    suggested_category = "Other"
    
    work_keywords = ["meeting", "report", "presentation", "slide", "project", "code", "email", "call", "schedule", "review", "office", "task"]
    shopping_keywords = ["buy", "shop", "groceries", "market", "store", "purchase", "order", "get", "milk", "food"]
    health_keywords = ["exercise", "run", "gym", "workout", "doctor", "dentist", "medicine", "pill", "sleep", "walk", "fitness"]
    finance_keywords = ["pay", "bill", "invoice", "rent", "tax", "salary", "budget", "bank", "card", "cost", "price"]
    personal_keywords = ["clean", "wash", "fix", "mom", "dad", "family", "gift", "book", "movie", "read", "watch", "friend"]
    
    if any(k in title_lower for k in work_keywords):
        suggested_category = "Work"
    elif any(k in title_lower for k in shopping_keywords):
        suggested_category = "Shopping"
    elif any(k in title_lower for k in health_keywords):
        suggested_category = "Health"
    elif any(k in title_lower for k in finance_keywords):
        suggested_category = "Finance"
    elif any(k in title_lower for k in personal_keywords):
        suggested_category = "Personal"
        
    # 2. Priority heuristics
    suggested_priority = "Medium"
    
    high_keywords = ["urgent", "asap", "deadline", "boss", "client", "important", "board", "presentation", "pay", "bill", "exam", "doctor", "now", "critical"]
    low_keywords = ["read", "watch", "buy", "clean", "movie", "book", "casual", "maybe", "later", "someday"]
    
    if any(k in title_lower for k in high_keywords):
        suggested_priority = "High"
    elif any(k in title_lower for k in low_keywords):
        suggested_priority = "Low"
        
    return suggested_category, suggested_priority
