from controllers import UserController, BookController, LoanController
from models import LoanBook
from utils import print_separator, add_space_to_camelcase


class BaseMenu:
    history = []
    current_user = None

    def __init__(self, db):
        self.db = db
        self.options = {}
        self.user_controller = UserController(self.db)
        self.book_controller = BookController(self.db)
        self.loan_controller = LoanController(self.db)

    def show_path(self):
        path = ' > '.join([add_space_to_camelcase(type(menu).__name__) for menu in self.history])
        print(path)

    @print_separator
    def display_menu(self):
        if not self.history or self.history[-1] != self:
            BaseMenu.history.append(self)
        self.show_path()

        for key, (option, _) in self.options.items():
            print(f'{key}. {option}')
        choice = input('Enter your choice: ')
        return choice

    def execute_choice(self, choice):
        if choice in self.options:
            _, action = self.options[choice]
            if isinstance(action, type):
                action(self.db).main_loop()
            else:
                action()
        else:
            print('Invalid choice')

    def register(self, is_admin=False):
        username = input('Enter username: ')
        password = input('Enter password: ')
        confirm_password = input('Confirm password: ')
        self.user_controller.create_user(username, password, confirm_password, is_admin)

    def back(self):
        if BaseMenu.history:
            BaseMenu.history.pop()
            if BaseMenu.history:
                BaseMenu.history[-1].main_loop()
            else:
                self.main_loop()
        else:
            print("No previous menu to return to.")
            self.main_loop()

    def logout(self):
        self.current_user = None
        self.history.clear()
        MainMenu(self.db).main_loop()

    def main_loop(self):
        while True:
            choice = self.display_menu()
            self.execute_choice(choice)


class MainMenu(BaseMenu):

    def __init__(self, db):
        super().__init__(db)
        self.options = {
            '1': ('register', self.register),
            '2': ('login', self.login),
            '3': ('exit', exit)
        }

    def login(self):
        username = input('Enter username: ')
        password = input('Enter password: ')
        user = self.user_controller.authenticate(username, password)
        if user:
            print('Login successful')
            BaseMenu.current_user = user
            self.user_menu_selector()
        else:
            print('Login failed')

    def user_menu_selector(self):
        if self.current_user['is_admin']:
            AdminMenu(self.db).main_loop()
        UserMenu(self.db).main_loop()


class AdminMenu(BaseMenu):

    def __init__(self, db):
        super().__init__(db)
        self.options = {
            '1': ('manage users', ManageUsersMenu),
            '2': ('manage books', ManageBooksMenu),
            '3': ('manage loans', ManageLoansMenu),
            '4': ('logout', self.logout)
        }


class UserMenu(BaseMenu):

    def __init__(self, db):
        super().__init__(db)
        self.options = {
            '1': ('books list', self.books_list),
            '2': ('loan book', self.loan_book),
            '3': ('return book', self.return_book),
            '4': ('logout', self.logout)
        }

    def books_list(self):
        genre = input('Enter genre: ')
        books = self.book_controller.get_books(genre)
        if books:
            for book in books:
                print(f'{book["id"]} {book["title"]}')
        else:
            print('No books found')

    def loan_book(self):
        book_id = int(input('Enter book id: '))
        book = self.book_controller.get_book(book_id)
        if book:
            self.loan_controller.create_loan(book_id, self.current_user['id'])
        else:
            print('Book not found')

    def return_book(self):
        loan_id = int(input('Enter loan id: '))
        loan = self.loan_controller.get_loan(loan_id)
        if loan:
            self.loan_controller.update_loan(loan_id, {'status': 'returned'})
        else:
            print('Loan not found')


class ManageUsersMenu(BaseMenu):

    def __init__(self, db):
        super().__init__(db)
        self.options = {
            '1': ('add user', self.register),
            '2': ('add admin', self.register),
            '3': ('edit user', self.edit_user),
            '4': ('delete user', self.delete_user),
            '5': ('users list', self.users_list),
            '6': ('back', self.back)
        }

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


class ManageBooksMenu(BaseMenu):

    def __init__(self, db):
        super().__init__(db)
        self.options = {
            '1': ('add book', self.add_book),
            '2': ('edit book', self.edit_book),
            '3': ('delete book', self.delete_book),
            '4': ('books list', self.books_list),
            '5': ('back', self.back)
        }

    def add_book(self):
        title = input('Enter title: ')
        author = input('Enter author: ')
        genre = input('Enter genre: ')
        isbn = input('Enter isbn: ')
        self.book_controller.create_book(title, author, genre, isbn)

    def edit_book(self):
        book_id = input('Enter book id: ')
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


class ManageLoansMenu(BaseMenu):

    def __init__(self, db):
        super().__init__(db)
        self.options = {
            '1': ('loans list', self.get_loans_by_status),
            '2': ('edit status', self.edit_loan_status),
            '3': ('back', self.back)
        }

    def get_loans_by_status(self, status='pending'):
        status = input(f'Enter status ({", ".join(LoanBook.Statuses)}): ')
        if status not in LoanBook.Statuses:
            print('Invalid status')
            return
        loans = self.loan_controller.get_loans(status)
        for loan in loans:
            if loan['status'] == 'pending':
                print(f'{loan["id"]} {loan["book"]["title"]}')

    def edit_loan_status(self):
        loan_id = int(input('Enter loan id: '))
        loan = self.loan_controller.get_loan(loan_id)
        if loan:
            status = input(f'Enter status ({", ".join(LoanBook.Statuses)}): ')
            if status not in LoanBook.Statuses:
                print('Invalid status')
                return
            self.loan_controller.update_loan(loan_id, {'status': status})
        else:
            print('Loan not found')
