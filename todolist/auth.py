import os
import json
import hashlib
import hmac
from datetime import datetime

USERS_FILE = os.path.join("data", "users.json")

def _ensure_store():
    """Ensure data directory and users.json file exist."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

def _load_users():
    """Load users from the JSON store."""
    _ensure_store()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_users(users):
    """Save users to the JSON store."""
    _ensure_store()
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def _hash_password(password, salt_hex=None):
    """
    Hash the password using PBKDF2-HMAC-SHA256 with 100,000 iterations.
    If salt_hex is None, generate a random 16-byte salt.
    """
    if salt_hex is None:
        salt = os.urandom(16)
    else:
        salt = bytes.fromhex(salt_hex)
        
    password_bytes = password.encode("utf-8")
    
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt,
        100000
    )
    
    return salt.hex(), password_hash.hex()

def register_user(username, password, confirm_password):
    """
    Validate and register a new user.
    Returns (success_boolean, feedback_message).
    """
    # 1. Basic validation
    if not username or len(username.strip()) < 3:
        return False, "Username must be at least 3 characters long."
        
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters long."
        
    if password != confirm_password:
        return False, "Passwords do not match."
        
    # Normalize username to lowercase for case-insensitivity
    normalized_username = username.strip().lower()
    
    users = _load_users()
    
    # Check if username is already taken
    if normalized_username in users:
        return False, "Username is already taken."
        
    # Hash password
    salt_hex, hash_hex = _hash_password(password)
    
    # Store user
    users[normalized_username] = {
        "salt": salt_hex,
        "password_hash": hash_hex,
        "created_at": datetime.now().isoformat()
    }
    
    _save_users(users)
    return True, "Registration successful! Please log in above."

def login_user(username, password):
    """
    Verify login credentials.
    Returns True if valid, False otherwise (timing-safe check).
    """
    if not username or not password:
        return False
        
    normalized_username = username.strip().lower()
    users = _load_users()
    
    # Look up user (generic error return to prevent user enumeration)
    if normalized_username not in users:
        return False
        
    stored_user = users[normalized_username]
    stored_salt = stored_user["salt"]
    stored_hash = stored_user["password_hash"]
    
    # Compute password hash with stored salt
    _, computed_hash = _hash_password(password, stored_salt)
    
    # Timing-safe comparison using hmac.compare_digest
    if hmac.compare_digest(computed_hash.encode("utf-8"), stored_hash.encode("utf-8")):
        return True
        
    return False
