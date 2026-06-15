import requests
from . import database
from .models import Admin, Member, Book, BorrowRecord

def execute_add_book():
    """Prompt admin for an ISBN, look it up on Open Library, and save it to the catalog."""
    print("\n--- ADD A NEW BOOK VIA ISBN ---")
    isbn = input("Enter 10 or 13 digit Book ISBN: ").strip()

    if not isbn:
        print("ISBN cannot be blank.")
        return

    db_data = database.load_raw_data()
    if any(b["isbn"] == isbn for b in db_data["books"]):
        print("This book already exists in your local library catalog.")
        return

    print(f"Connecting to Open Library to look up ISBN: {isbn}...")
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("Could not connect to the external book service.")
            return
    except requests.exceptions.RequestException:
        print("Network error. Check your internet connection.")
        return

    data = response.json()
    isbn_key = f"ISBN:{isbn}"

    if isbn_key not in data:
        print("No book found matching that ISBN in the global database.")
        return

    book_info = data[isbn_key]
    title = book_info.get("title", "Unknown Title")
    authors_list = book_info.get("authors", [])
    author = authors_list[0].get("name", "Unknown Author") if authors_list else "Unknown Author"

    print(f"Found: '{title}' by {author}")

    try:
        copies = int(input("Enter number of physical copies to add: "))
        if copies < 1:
            print("Must add at least 1 copy. Aborted.")
            return
    except ValueError:
        print("Invalid number. Book creation aborted.")
        return

    new_book = Book(title, author, isbn, copies)
    db_data["books"].append(new_book.to_dict())
    database.save_raw_data(db_data)

    print(f"Success! '{title}' has been added to the catalog with {copies} copy/copies.")

def execute_remove_book():
    """Prompt admin for a book title and permanently remove it from the catalog."""
    print("\n--- REMOVE A BOOK ---")
    title = input("Enter the title of the book to remove: ").strip()

    if not title:
        print("Title cannot be blank.")
        return

    db_data = database.load_raw_data()
    book_to_remove = next(
        (b for b in db_data["books"] if b["title"].lower() == title.lower()), None
    )

    if not book_to_remove:
        print(f"Error: Book '{title}' not found in the catalog.")
        return

    isbn = book_to_remove["isbn"]
    print(f"\nBook found: '{book_to_remove['title']}' by {book_to_remove['author']}")
    confirm = input("Are you sure you want to remove this book? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Removal cancelled.")
        return
    db_data["books"] = [b for b in db_data["books"] if b["isbn"] != isbn]
    db_data["borrows"] = [r for r in db_data["borrows"] if r["isbn"] != isbn]
    for member in db_data.get("members", []):
        if isbn in member.get("borrowed_isbns", []):
            member["borrowed_isbns"].remove(isbn)

    database.save_raw_data(db_data)
    print(f"\nSuccess: '{book_to_remove['title']}' has been removed from the library.")

def execute_search_books():
    """Search the catalog by title or author and display matching books."""
    print("\n--- SEARCH BOOKS ---")
    print("1. Search by Title")
    print("2. Search by Author")
    choice = input("Select an option (1-2): ").strip()

    if choice not in ("1", "2"):
        print("Invalid option.")
        return

    query = input("Enter search term: ").strip().lower()
    if not query:
        print("Search term cannot be blank.")
        return

    db_data = database.load_raw_data()
    books = db_data["books"]

    if choice == "1":
        results = [b for b in books if query in b["title"].lower()]
    else:
        results = [b for b in books if query in b["author"].lower()]

    if not results:
        print(f"\nNo books found matching '{query}'.")
        return

    print(f"\n--- {len(results)} Result(s) Found ---")
    for b in results:
        status = f"{b['available_copies']} copy/copies available" if b["available_copies"] > 0 else "Not available"
        print(f"  Title  : {b['title']}")
        print(f"  Author : {b['author']}")
        print(f"  ISBN   : {b['isbn']}")
        print(f"  Status : {status}")
        print("  " + "-" * 30)

def execute_borrow_book(current_user):
    """
    Prompt a member for an ISBN, check availability,
    record the borrow, and update the member's borrowed list.
    """
    print("\n--- BORROW A BOOK ---")
    isbn = input("Enter the ISBN of the book you want to borrow: ").strip()

    if not isbn:
        print("ISBN cannot be blank.")
        return

    db_data = database.load_raw_data()
    book_dict = next((b for b in db_data["books"] if b["isbn"] == isbn), None)

    if not book_dict:
        print(f"No book with ISBN '{isbn}' found in the catalog.")
        return

    book = Book.from_dict(book_dict)

    if not book.is_available():
        print(f"Sorry, '{book.title}' has no available copies right now.")
        return
    member_dict = next(
        (m for m in db_data.get("members", []) if m["username"] == current_user.username), None
    )

    if member_dict and isbn in member_dict.get("borrowed_isbns", []):
        print("You have already borrowed this book.")
        return
    book_dict["available_copies"] -= 1
    if member_dict:
        member_dict.setdefault("borrowed_isbns", []).append(isbn)
    new_record = BorrowRecord(current_user.username, isbn)
    db_data["borrows"].append(new_record.to_dict())

    database.save_raw_data(db_data)
    print(f"Success! You have borrowed '{book.title}'. Enjoy your read!")

def execute_return_book(current_user):
    """
    Prompt a member for an ISBN, verify they borrowed it,
    mark the borrow record as returned, and restore available copies.
    """
    print("\n--- RETURN A BOOK ---")
    isbn = input("Enter the ISBN of the book you are returning: ").strip()

    if not isbn:
        print("ISBN cannot be blank.")
        return

    db_data = database.load_raw_data()
    member_dict = next(
        (m for m in db_data.get("members", []) if m["username"] == current_user.username), None
    )

    if not member_dict or isbn not in member_dict.get("borrowed_isbns", []):
        print(f"You do not have a book with ISBN '{isbn}' in your borrowed list.")
        return
    book_dict = next((b for b in db_data["books"] if b["isbn"] == isbn), None)

    if book_dict:
        book_dict["available_copies"] += 1
    member_dict["borrowed_isbns"].remove(isbn)
    for record in db_data["borrows"]:
        if (record["username"] == current_user.username
                and record["isbn"] == isbn
                and record["return_date"] is None):
            borrow_record = BorrowRecord.from_dict(record)
            borrow_record.mark_returned()
            record["return_date"] = borrow_record.return_date
            break

    database.save_raw_data(db_data)
    title = book_dict["title"] if book_dict else isbn
    print(f"Success! '{title}' has been returned. Thank you!")

def execute_view_borrowed_books(current_user):
    """Display full details of all books currently borrowed by the member."""
    print("\n--- MY BORROWED BOOKS ---")

    db_data = database.load_raw_data()
    member_dict = next(
        (m for m in db_data.get("members", []) if m["username"] == current_user.username), None
    )

    if not member_dict:
        print("Member record not found.")
        return

    borrowed_isbns = member_dict.get("borrowed_isbns", [])

    if not borrowed_isbns:
        print("You have no borrowed books at the moment.")
        return

    print(f"\nYou currently have {len(borrowed_isbns)} borrowed book(s):\n")
    for isbn in borrowed_isbns:
        book_dict = next((b for b in db_data["books"] if b["isbn"] == isbn), None)
        borrow_record = next(
            (r for r in db_data["borrows"]
             if r["username"] == current_user.username and r["isbn"] == isbn and r["return_date"] is None),
            None
        )
        if book_dict:
            print(f"  Title      : {book_dict['title']}")
            print(f"  Author     : {book_dict['author']}")
            print(f"  ISBN       : {isbn}")
            if borrow_record:
                print(f"  Borrowed on: {borrow_record['borrow_date']}")
            print("  " + "-" * 30)
        else:
            print(f"  ISBN: {isbn} (book details not found)")
            print("  " + "-" * 30)

def standalone_menu():
    """Quick test interface — run library.py directly to test functions."""
    while True:
        print("\n--- ENGINE STANDALONE INTERFACE ---")
        print("1. Add a Book (Admin)")
        print("2. Remove a Book (Admin)")
        print("3. Search Books")
        print("4. Exit Test")
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            execute_add_book()
        elif choice == "2":
            execute_remove_book()
        elif choice == "3":
            execute_search_books()
        elif choice == "4":
            print("Exiting standalone test.")
            break
        else:
            print("Invalid option.")