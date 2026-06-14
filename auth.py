import bcrypt
from library_management import database
from library_management.models import Member, Admin

def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password, stored_hash):
    password_bytes = plain_password.encode("utf-8")
    hash_bytes = stored_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)

def register(username, password):
    db_data = database.load_raw_data()
    existing_users = db_data["members"]
    for user in existing_users:
        if user["username"] == username:
            print("Username already exists. Please choose another.")
            return False
    hashed = hash_password(password)
    new_member = Member(username, hashed)
    db_data["members"].append(new_member.to_dict())
    database.save_raw_data(db_data)
    print(f"Account created successfully! Welcome, {username}.")
    return True

def login(username, password):
    db_data = database.load_raw_data()
    user_dict = next((u for u in db_data["members"]
                      if u["username"] == username), None)
    if not user_dict:
        print("Username not found.")
        return None
    if not verify_password(password, user_dict["password_hash"]):
        print("Incorrect password.")
        return None
    if user_dict["role"] == "admin":
        print(f"\nWelcome back, Admin {username}!")
        return Admin.from_dict(user_dict)
    elif user_dict["role"] == "member":
        print(f"\nWelcome back, Member {username}!")
        return Member.from_dict(user_dict)
    return None

def admin_required(func):
    def wrapper(user, *args, **kwargs):
        if user.role != "admin":
            print("Access denied. Admins only.")
            return None
        return func(user, *args, **kwargs)
    return wrapper
