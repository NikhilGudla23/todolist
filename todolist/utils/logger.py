import os
from datetime import datetime

LOG_FILE = os.path.join("database", "app.log")

def _write_log(level, message):
    """Internal helper to write timestamped logs to a file."""
    try:
        os.makedirs("database", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"[Logger Fail] [{level}] {message} (Error: {e})")

def info(message):
    """Log informational message."""
    _write_log("INFO", message)

def warning(message):
    """Log warning message."""
    _write_log("WARNING", message)

def error(message):
    """Log error message."""
    _write_log("ERROR", message)
