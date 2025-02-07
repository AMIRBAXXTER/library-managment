import base64

import bcrypt
import json
import os
import re
import config


def validate_password(password, confirm_password):
    massages = []
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(pattern, password):
        massages.append(
            'Password must contain at least one uppercase letter, one lowercase letter, one number and one special character')
    if len(password) < 8:
        massages.append('Password must be at least 8 characters')
    if password != confirm_password:
        massages.append('Passwords do not match')

    if massages:
        for message in massages:
            print(message)
        return None
    return password


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return base64.b64encode(hashed_password).decode('utf-8')


def check_password(input_password, hashed_password):
    hashed_password = base64.b64decode(hashed_password)
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)


class LoadOrInitializeMixin:

    def __init__(self):
        self.file_dir = None

    def _load_or_initialize_data(self):
        if not os.path.exists(self.file_dir):
            os.makedirs(os.path.dirname(self.file_dir), exist_ok=True)
            with open(self.file_dir, 'w') as file:
                json.dump({}, file)
        with open(self.file_dir, 'r') as file:
            return json.load(file)


class IDManager(LoadOrInitializeMixin):
    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(IDManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        super().__init__()
        self.file_dir = 'data/ids.json'
        self.ids = self._load_or_initialize_data()

    def _write_ids(self):

        with open(self.file_dir, 'w') as file:
            json.dump(self.ids, file, indent=4)

    def get_id(self, entity_class):

        if entity_class not in self.ids:
            self.ids[entity_class] = 0
        self.ids[entity_class] += 1
        self._write_ids()
        return self.ids[entity_class]


def print_stars(func):
    def wrapper(*args, **kwargs):
        print(config.SEPERATOR_CHAR * 50)
        result = func(*args, **kwargs)
        print(config.SEPERATOR_CHAR * 50)
        return result

    return wrapper


class DecoratedMethodsMeta(type):

    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                attrs[attr_name] = print_stars(attr_value)
        return super().__new__(cls, name, bases, attrs)
