from json_database import JsonDatabase
from models import User, Book, LoanBook

if __name__ == '__main__':
    db = JsonDatabase()
    users = db.all(User)
    for user in users:
        print(user['username'])
