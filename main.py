from library_management import database, Admin, Member

def authenticate_user():
    print("\n=== WELCOME TO THE LIBRARY ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    db_data = database.load_raw_data()
    
    user_dict = next((u for u in db_data["members"] if u["username"] == username), None)
    
    if not user_dict:
        print("Username not found.")
        return None

    if user_dict["password_hash"] != password:
        print("Incorrect password.")
        return None

    if user_dict["role"] == "admin":
        print(f"\nWelcome back, Admin {username}!")
        return Admin.from_dict(user_dict)
    elif user_dict["role"] == "member":
        print(f"\nWelcome back, Member {username}!")
        return Member.from_dict(user_dict)
        
    return None

def show_admin_menu(admin_user):
    while True:
        print(f"\n--- ADMIN MENU ({admin_user.username}) ---")
        print("1. Add a New Book")
        print("2. Remove a Book")
        print("3. Logout")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            print("\n[Feature coming soon: Add Book Logic]")
        elif choice == "2":
            print("\n[Feature coming soon: Remove Book Logic]")
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice, try again.")

def show_member_menu(member_user):
    while True:
        print(f"\n--- MEMBER MENU ({member_user.username}) ---")
        print("1. Borrow a Book")
        print("2. Return a Book")
        print("3. View My Borrowed Books")
        print("4. Logout")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            print("\n[Feature coming soon: Borrow Book Logic]")
        elif choice == "2":
            print("\n[Feature coming soon: Return Book Logic]")
        elif choice == "3":
            print(f"\nYour borrowed ISBNs: {member_user.get_borrowed_books()}")
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice, try again.")

def main():
    current_user = None
    
    while True:
        if current_user is None:
            current_user = authenticate_user()
            continue 
            
        if current_user.role == "admin":
            show_admin_menu(current_user)
            current_user = None
            
        elif current_user.role == "member":
            show_member_menu(current_user)
            current_user = None 

if __name__ == "__main__":
    main()