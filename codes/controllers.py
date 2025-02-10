from models import User, Book, LoanBook
import hashlib
import os
from utils import validate_password, hash_password, check_password


class UserController:

    def __init__(self, db):
        self.db = db

    def create_user(self, username, password, confirm_password, is_admin=False):

        v_password = validate_password(password, confirm_password)

        if v_password:
            hashed_password = hash_password(v_password)
            user = User(username, hashed_password)
            user.is_admin = is_admin
            created = self.db.save(user)
            if created:
                print(f'User {username} created')

    def update_user(self, user_id, values: dict):
        user = self.db.update(User, user_id, values)
        if user:
            print(f'User {user_id} updated')

    def delete_user(self, user_id):
        self.db.delete(User, user_id)
        print(f'User {user_id} deleted')

    def authenticate(self, username, password):
        user = self.db.filter(User, username=username)
        if user:
            user = user[0]
            if check_password(password, user['password']):
                return user
        else:
            print('Username or Password is incorrect')
        return None

    def get_user(self, user_id):
        return self.db.get(User, user_id)

    def get_users(self):
        return self.db.all(User)


class BookController:

    def __init__(self, db):
        self.db = db

    def create_book(self, title, author, isbn):
        book = Book(title, author, isbn)
        created = self.db.save(book)
        if created:
            print(f'Book {title} created')

    def update_book(self, book_id, values: dict):
        book = self.db.update(Book, book_id, values)
        if book:
            print(f'Book {book_id} updated')

    def delete_book(self, book_id):
        self.db.delete(Book, book_id)
        print(f'Book {book_id} deleted')

    def get_book(self, book_id):
        return self.db.get(Book, book_id)

    def get_books(self):
        return self.db.all(Book)


class LoanController:

    def __init__(self, db):
        self.db = db

    def create_loan(self, book_id, user_id, status='pending'):
        book = self.db.get(Book, book_id)
        user = self.db.get(User, user_id)
        if book and user:
            loan = LoanBook(book_id, user_id, status)
            created = self.db.save(loan)
            if created:
                print(f'Loan {book_id} created')

    def update_loan(self, loan_id, values: dict):
        loan = self.db.update(LoanBook, loan_id, values)
        if loan:
            print(f'Loan {loan_id} updated')

    def get_loan(self, loan_id):
        return self.db.get(LoanBook, loan_id)

    def get_loans(self, status='pending'):
        return self.db.filter(LoanBook, status=status)
