import re

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

def validate_email(email):
    """
    Check if email matches typical standards.
    """
    if not email:
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))

def validate_username(username):
    """
    Username must be at least 3 characters long and alphanumeric (plus underscores).
    """
    if not username:
        return False
    username_stripped = username.strip()
    if len(username_stripped) < 3:
        return False
    return bool(re.match(r"^[a-zA-Z0-9_]+$", username_stripped))

def validate_password(password):
    """
    Password must be at least 4 characters long.
    """
    if not password:
        return False
    return len(password) >= 4

def validate_task_title(title):
    """
    Task title must be non-empty and under 100 characters.
    """
    if not title or not title.strip():
        return False
    return len(title.strip()) <= 100

def validate_task_description(description):
    """
    Task description must be under 500 characters.
    """
    if description is None:
        return True
    return len(description) <= 500
