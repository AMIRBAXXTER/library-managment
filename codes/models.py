class User:
    UniqueFields = ['username']

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.is_available = True
        self.isbn = isbn


class LoanBook:
    def __init__(self, user: User, book: Book, loan_date, return_date):
        self.user = user
        self.book = book
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False
