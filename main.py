from library_management import database
from library_management.models import Admin, Member
from auth import register, login
 

def show_opening_menu():
    while True:
        print("\n=== WELCOME TO THE LIBRARY ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = login(username, password)
            if user:
                return user
        elif choice == "2":
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            register(username, password)
            print("Please login with your new account.")
        elif choice == "3":
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice, try again.")
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
            current_user = show_opening_menu()
            continue
            
        if current_user.role == "admin":
            show_admin_menu(current_user)
            current_user = None
            
        elif current_user.role == "member":
            show_member_menu(current_user)
            current_user = None

if __name__ == "__main__":
    main()