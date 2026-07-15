from datetime import datetime, date
from utils.constants import CATEGORY_ICONS

def format_date(iso_string, include_time=True):
    """Format ISO timestamp to readable text."""
    if not iso_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_string)
        if include_time:
            return dt.strftime("%b %d, %Y %I:%M %p")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return iso_string

def get_category_icon(category):
    """Get emoji icon for a specific task category."""
    return CATEGORY_ICONS.get(category, "📁")

def truncate_text(text, limit=40):
    """Truncate text to a specific character length."""
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit] + "..."

def get_relative_due_date(due_date_str):
    """
    Returns a dynamic relative countdown string based on the due date.
    E.g. "Due Today", "Due Tomorrow", "Overdue by 3 days", "In 5 days".
    """
    if not due_date_str:
        return "📅 No Deadline"
        
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        today = date.today()
        diff = (due_date - today).days
        
        if diff == 0:
            return "⏳ Due Today"
        elif diff == 1:
            return "⏳ Due Tomorrow"
        elif diff == -1:
            return "🚨 Overdue by 1 day"
        elif diff < -1:
            return f"🚨 Overdue by {abs(diff)} days"
        else:
            return f"📅 In {diff} days"
    except Exception:
        return f"📅 {due_date_str}"

def get_user_level(completed_count):
    """
    Return gamified user level name and avatar icon based on lifetime completions.
    """
    if completed_count == 0:
        return "Task Explorer 🥚", "Lv.0"
    elif completed_count <= 5:
        return "Efficiency Scout 🛠️", "Lv.1"
    elif completed_count <= 15:
        return "Productivity Knight ⚔️", "Lv.2"
    else:
        return "Taskmaster Emperor 👑", "Lv.3"
