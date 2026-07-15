import uuid
from datetime import datetime
import bcrypt
import utils.database as db
import utils.validation as val
import utils.session as sess
import utils.logger as log

def register_user(name, username, email, password, confirm_password):
    """
    Validate and register a new user in the JSON database.
    Returns (success_boolean, message).
    """
    # 1. Strip and normalize inputs
    name_clean = name.strip() if name else ""
    username_clean = username.strip().lower() if username else ""
    email_clean = email.strip().lower() if email else ""
    
    # 2. Input validation
    if not name_clean:
        return False, "Full Name is required."
        
    if not val.validate_username(username_clean):
        return False, "Username must be at least 3 characters and contain only letters, numbers, or underscores."
        
    if not val.validate_email(email_clean):
        return False, "Please enter a valid email address."
        
    if not val.validate_password(password):
        return False, "Password must be at least 4 characters long."
        
    if password != confirm_password:
        return False, "Passwords do not match."
        
    try:
        users = db.read_json(db.USERS_FILE)
        
        # Check uniqueness (case-insensitive)
        for user in users:
            if user["username"] == username_clean:
                return False, "Username is already taken."
            if user["email"] == email_clean:
                return False, "Email address is already registered."
                
        # Hash password using bcrypt
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
        hashed_password = hashed_bytes.decode("utf-8")
        
        # Create user record
        new_user = {
            "id": str(uuid.uuid4()),
            "name": name_clean,
            "username": username_clean,
            "email": email_clean,
            "password": hashed_password,
            "created_at": datetime.now().isoformat()
        }
        
        users.append(new_user)
        db.write_json(db.USERS_FILE, users)
        
        log.info(f"Registered user: {username_clean} ({email_clean})")
        return True, "Account created successfully! Please log in."
        
    except Exception as e:
        log.error(f"Error during registration: {e}")
        return False, "A system error occurred. Please try again later."

def login_user(username, password):
    """
    Authenticate a user.
    On success, starts the session and returns True. Otherwise, returns False.
    """
    username_clean = username.strip().lower() if username else ""
    
    if not username_clean or not password:
        return False
        
    try:
        users = db.read_json(db.USERS_FILE)
        
        # Find user record (generic error response for security)
        user_record = None
        for user in users:
            if user["username"] == username_clean:
                user_record = user
                break
                
        if not user_record:
            return False
            
        # Verify bcrypt password
        hashed_stored = user_record["password"]
        if bcrypt.checkpw(password.encode("utf-8"), hashed_stored.encode("utf-8")):
            sess.login(user_record)
            log.info(f"User logged in: {username_clean}")
            return True
            
        return False
        
    except Exception as e:
        log.error(f"Error during login verification: {e}")
        return False
