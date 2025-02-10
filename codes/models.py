from datetime import datetime


class User:
    UniqueFields = ['username']

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_admin = False


class Book:
    def __init__(self, title, author, genre, isbn):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_available = True
        self.isbn = isbn


class LoanBook:
    Statuses = ['pending', 'approved', 'declined', 'returned']

    def __init__(self, user: User, book: Book):
        self.user = user
        self.book = book
        self.loan_request_date = datetime.now()
        self.loan_approval_date = None
        self.loan_return_date = None
        self.status = LoanBook.Statuses[0]
