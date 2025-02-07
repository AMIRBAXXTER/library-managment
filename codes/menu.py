import config
from controllers import UserController, BookController, LoanController
from models import User, LoanBook
from utils import DecoratedMethodsMeta


class Menu(metaclass=DecoratedMethodsMeta):

    def __init__(self, db):
        self.db = db
        self.user_controller = UserController(self.db)
        self.book_controller = BookController(self.db)
        self.loan_controller = LoanController(self.db)
        self.current_user = None

    def main_menu(self):
        while True:
            print(f'{config.APP_NAME}\n 1. Register \n 2. Login \n 3. Exit')
            choice = (input('Enter your choice: '))
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                break
            else:
                print('Invalid choice')
                continue

    def register(self, is_admin=False):
        username = input('Enter username: ')
        password = input('Enter password: ')
        confirm_password = input('Confirm password: ')
        self.user_controller.create_user(username, password, confirm_password, is_admin)

    def login(self):
        username = input('Enter username: ')
        password = input('Enter password: ')
        user = self.user_controller.authenticate(username, password)
        if user:
            print('Login successful')
            self.current_user = user
            self.user_menu_selector()
        else:
            print('Login failed')

    def user_menu_selector(self):
        if self.current_user['is_admin']:
            self.admin_menu()
        self.user_menu()

    def admin_menu(self):
        while True:
            print('Admin Menu \n 1. Manage Users \n 2. Manage Books \n 3. Manage Loans \n 4. Logout')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                self.manage_users_menu()
            elif choice == 2:
                self.manage_books_menu()
            elif choice == 3:
                self.manage_loans_menu()
            elif choice == 4:
                self.current_user = None
                self.main_menu()
                break
            else:
                print('Invalid choice')
                continue

    def manage_users_menu(self):
        while True:
            print(
                'Manage Users \n 1. Add User \n 2. Add Admin 3. Edit User \n 4. Delete User 5. Users List  \n 6. Back')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                self.register()
            elif choice == 2:
                self.register(is_admin=True)
            elif choice == 3:
                self.edit_user()
            elif choice == 4:
                self.delete_user()
            elif choice == 5:
                self.users_list()
            elif choice == 6:
                break
            else:
                print('Invalid choice')
                continue

    def edit_user(self):
        user_id = int(input('Enter user id: '))
        user = self.user_controller.get_user(user_id)
        if user:
            username = input('Enter username: ')
            password = input('Enter password: ')
            confirm_password = input('Confirm password: ')
            self.user_controller.update_user(user_id, {'username': username, 'password': password,
                                                       'confirm_password': confirm_password})

    def delete_user(self):
        user_id = int(input('Enter user id: '))
        self.user_controller.delete_user(user_id)

    def users_list(self):
        users = self.user_controller.get_users()
        for user in users:
            print(f'{user["id"]} {user["username"]}')

    def manage_books_menu(self):
        while True:
            print('Manage Books \n 1. Add Book \n 2. Edit Book \n 3. Delete Book \n 4. Books List \n 5. Back')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.edit_book()
            elif choice == 3:
                self.delete_book()
            elif choice == 4:
                self.books_list()
            elif choice == 5:
                break
            else:
                print('Invalid choice')
                continue

    def add_book(self):
        title = input('Enter title: ')
        author = input('Enter author: ')
        isbn = input('Enter isbn: ')
        self.book_controller.create_book(title, author, isbn)

    def edit_book(self):
        book_id = int(input('Enter book id: '))
        book = self.book_controller.get_book(book_id)
        if book:
            title = input('Enter title: ')
            author = input('Enter author: ')
            isbn = input('Enter isbn: ')
            self.book_controller.update_book(book_id, {'title': title, 'author': author, 'isbn': isbn})

    def delete_book(self):
        book_id = int(input('Enter book id: '))
        self.book_controller.delete_book(book_id)

    def books_list(self):
        books = self.book_controller.get_books()
        for book in books:
            print(f'{book["id"]} {book["title"]}')

    def manage_loans_menu(self):
        while True:
            print(
                'Manage Loans \n 1. Pending \n 2. Approved \n 3. Declined \n 4. Returned \n 5. Edit Status \n 6. Back')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                self.get_loans_by_status('pending')
            elif choice == 2:
                self.get_loans_by_status('approved')
            elif choice == 3:
                self.get_loans_by_status('declined')
            elif choice == 4:
                self.get_loans_by_status('returned')
            elif choice == 5:
                self.edit_loan_status()
            elif choice == 6:
                break
            else:
                print('Invalid choice')
                continue

    def get_loans_by_status(self, status='pending'):
        loans = self.loan_controller.get_loans(status)
        for loan in loans:
            if loan['status'] == 'pending':
                print(f'{loan["id"]} {loan["book"]["title"]}')

    def edit_loan_status(self):
        loan_id = int(input('Enter loan id: '))
        loan = self.loan_controller.get_loan(loan_id)
        if loan:
            statuses = LoanBook.Statuses
            status = input(f'Enter status ({", ".join(statuses)}): ')
            self.loan_controller.update_loan(loan_id, {'status': status})

    def user_menu(self):
        while True:
            print('User Menu \n 1. Loan Book \n 2. Return Book \n 3. Logout')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                self.loan_book()
            elif choice == 2:
                self.return_book()
            elif choice == 3:
                self.current_user = None
                self.main_menu()
                break
            else:
                print('Invalid choice')
                continue

    def loan_book(self):
        pass

    def return_book(self):
        pass
