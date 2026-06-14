import datetime

class User:
    def __init__(self, username, password_hash, role):
        self.username = username
        self._password_hash = password_hash
        self.role = role

    def check_password(self, password):
        return self._password_hash == password

    def to_dict(self):
        return {"username": self.username, "password_hash": self._password_hash, "role": self.role}

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password_hash"])


class Admin(User):
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, role="admin")


class Member(User):
    def __init__(self, username, password_hash, borrowed_isbns=None):
        super().__init__(username, password_hash, role="member")
        self._borrowed_isbns = borrowed_isbns if borrowed_isbns is not None else []

    def borrow_book(self, isbn, book):
        if book.is_available() and isbn not in self._borrowed_isbns:
            self._borrowed_isbns.append(isbn)
            book._available_copies -= 1
            return True
        return False

    def return_book(self, isbn, book):
        if isbn in self._borrowed_isbns:
            self._borrowed_isbns.remove(isbn)
            book._available_copies += 1
            return True
        return False

    def get_borrowed_books(self):
        return self._borrowed_isbns

    def to_dict(self):
        data = super().to_dict()
        data["borrowed_isbns"] = self._borrowed_isbns
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password_hash"])


class Book:
    def __init__(self, title, author, isbn, available_copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._available_copies = available_copies

    def is_available(self):
        return self._available_copies > 0

    @property
    def available_copies(self):
        return self._available_copies

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "available_copies": self._available_copies}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["isbn"], data["available_copies"])


class BorrowRecord:
    def __init__(self, username, isbn, borrow_date=None, return_date=None):
        self.username = username
        self.isbn = isbn
        self.borrow_date = borrow_date if borrow_date else datetime.date.today().isoformat()
        self.return_date = return_date

    def mark_returned(self):
        self.return_date = datetime.date.today().isoformat()

    def to_dict(self):
        return {"username": self.username, "isbn": self.isbn, "borrow_date": self.borrow_date, "return_date": self.return_date}

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["isbn"], data["borrow_date"], data["return_date"])