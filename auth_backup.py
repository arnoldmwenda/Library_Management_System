import bcrypt
from library_management import database
from library_management.models import Member, Admin

# ---- PASSWORD HASHING ----

def hash_password(password):
    """Convert plain text password to a secure hash."""
    # encode converts string → bytes (bcrypt requires bytes)
    password_bytes = password.encode("utf-8")
    # gensalt() generates random salt, hashpw() does the hashing
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # decode converts bytes back to string so it can be saved in JSON
    return hashed.decode("utf-8")


def verify_password(plain_password, stored_hash):
    """Check if a plain text password matches the stored hash."""
    # convert both to bytes - bcrypt requires bytes not strings
    password_bytes = plain_password.encode("utf-8")
    hash_bytes = stored_hash.encode("utf-8")
    # checkpw handles the comparison securely
    return bcrypt.checkpw(password_bytes, hash_bytes)


def register(username, password):
    """Register a new member account."""
    # Step 1: load existing data from JSON
    db_data = database.load_raw_data()
    
    # Step 2: check if username already exists
    existing_users = db_data["members"]
    for user in existing_users:
        if user["username"] == username:
            print("Username already exists. Please choose another.")
            return False
    
    # Step 3: hash the password using our function
    hashed = hash_password(password)
    
    # Step 4: create a new Member object
    new_member = Member(username, hashed)
    
    # Step 5: convert to dict and append to members list
    db_data["members"].append(new_member.to_dict())
    
    # Step 6: save back to JSON
    database.save_raw_data(db_data)
    
    print(f"Account created successfully! Welcome, {username}.")
    return True


def login(username, password):
    """Login an existing user and return the correct object."""
    # Step 1: load existing data from JSON
    db_data = database.load_raw_data()
    
    # Step 2: search for the username
    user_dict = next((u for u in db_data["members"] 
                      if u["username"] == username), None)
    
    # Step 3: if username not found
    if not user_dict:
        print("Username not found.")
        return None
    
    # Step 4: verify the password
    if not verify_password(password, user_dict["password_hash"]):
        print("Incorrect password.")
        return None
    
    # Step 5: return correct object based on role
    if user_dict["role"] == "admin":
        print(f"\nWelcome back, Admin {username}!")
        return Admin.from_dict(user_dict)
    elif user_dict["role"] == "member":
        print(f"\nWelcome back, Member {username}!")
        return Member.from_dict(user_dict)
    
    return None

def admin_required(func):
    """Decorator that blocks non-admin users from calling a function."""
    def wrapper(user, *args, **kwargs):
        # check the role BEFORE running the function
        if user.role != "admin":
            print("Access denied. Admins only.")
            return None
        # if they are admin, run the function normally
        return func(user, *args, **kwargs)
    return wrapper