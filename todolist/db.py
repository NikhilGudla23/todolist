import os
import json
import uuid
from datetime import datetime

TODOS_FILE = os.path.join("data", "todos.json")

def _ensure_store():
    """Ensure data directory and todos.json file exist."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

def _load_todos():
    """Load todos from the JSON store."""
    _ensure_store()
    try:
        with open(TODOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_todos(todos):
    """Save todos to the JSON store."""
    _ensure_store()
    with open(TODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)

def get_active_todos(username):
    """
    Get all active (pending) todos for a user.
    """
    normalized_username = username.strip().lower()
    todos_db = _load_todos()
    user_todos = todos_db.get(normalized_username, [])
    return [todo for todo in user_todos if todo.get("status") == "pending"]

def get_history_todos(username):
    """
    Get all completed todos for a user.
    """
    normalized_username = username.strip().lower()
    todos_db = _load_todos()
    user_todos = todos_db.get(normalized_username, [])
    return [todo for todo in user_todos if todo.get("status") == "completed"]

def add_todo(username, task_text, priority):
    """
    Prepend a new todo to the user's todo list.
    """
    if not task_text or not task_text.strip():
        return False
        
    normalized_username = username.strip().lower()
    todos_db = _load_todos()
    
    if normalized_username not in todos_db:
        todos_db[normalized_username] = []
        
    new_todo = {
        "id": str(uuid.uuid4()),
        "task": task_text.strip(),
        "priority": priority, # "Low" | "Medium" | "High"
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    # Prepend to the list so newer tasks appear first
    todos_db[normalized_username].insert(0, new_todo)
    _save_todos(todos_db)
    return True

def complete_todo(username, todo_id):
    """
    Mark a todo item as completed.
    """
    normalized_username = username.strip().lower()
    todos_db = _load_todos()
    user_todos = todos_db.get(normalized_username, [])
    
    for todo in user_todos:
        if todo.get("id") == todo_id:
            todo["status"] = "completed"
            todo["completed_at"] = datetime.now().isoformat()
            break
            
    _save_todos(todos_db)

def restore_todo(username, todo_id):
    """
    Restore a completed todo item to pending.
    """
    normalized_username = username.strip().lower()
    todos_db = _load_todos()
    user_todos = todos_db.get(normalized_username, [])
    
    for todo in user_todos:
        if todo.get("id") == todo_id:
            todo["status"] = "pending"
            todo["completed_at"] = None
            break
            
    _save_todos(todos_db)

def delete_todo_permanently(username, todo_id):
    """
    Delete a todo item permanently from the database.
    """
    normalized_username = username.strip().lower()
    todos_db = _load_todos()
    user_todos = todos_db.get(normalized_username, [])
    
    # Filter out the todo to delete
    updated_todos = [todo for todo in user_todos if todo.get("id") != todo_id]
    
    todos_db[normalized_username] = updated_todos
    _save_todos(todos_db)

def clear_history(username):
    """
    Delete all completed todo items permanently for a user.
    """
    normalized_username = username.strip().lower()
    todos_db = _load_todos()
    user_todos = todos_db.get(normalized_username, [])
    
    # Keep only pending tasks
    updated_todos = [todo for todo in user_todos if todo.get("status") != "completed"]
    
    todos_db[normalized_username] = updated_todos
    _save_todos(todos_db)
