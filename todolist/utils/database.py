import os
import json
import tempfile

DB_DIR = "database"
USERS_FILE = os.path.join(DB_DIR, "users.json")
TASKS_FILE = os.path.join(DB_DIR, "tasks.json")
HISTORY_FILE = os.path.join(DB_DIR, "history.json")
SETTINGS_FILE = os.path.join(DB_DIR, "settings.json")

def ensure_store():
    """Ensure database directory and files exist with correct default structures."""
    os.makedirs(DB_DIR, exist_ok=True)
    
    for filepath, default_val in [
        (USERS_FILE, []),
        (TASKS_FILE, []),
        (HISTORY_FILE, []),
        (SETTINGS_FILE, {})
    ]:
        if not os.path.exists(filepath):
            write_json(filepath, default_val)

def read_json(filepath):
    """Safely read and parse a JSON file with exception handling."""
    ensure_store()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Corrupted or missing file recovery
        default_val = {} if "settings" in filepath else []
        write_json(filepath, default_val)
        return default_val

def write_json(filepath, data):
    """Safely write data to a JSON file atomically using a temporary file."""
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    # Create temporary file in the target directory to allow atomic rename
    fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        # Atomic replacement of target file
        os.replace(temp_path, filepath)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise IOError(f"Failed writing to database path '{filepath}': {e}")
