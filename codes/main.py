from json_database import JsonDatabase
from menu import Menu

if __name__ == '__main__':
    db = JsonDatabase()
    menu = Menu(db)
    menu.main_menu()
