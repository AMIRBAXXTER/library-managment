from json_database import JsonDatabase
from menu import MainMenu

if __name__ == '__main__':
    db = JsonDatabase()
    menu = MainMenu(db)
    menu.main_loop()
