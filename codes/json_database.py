import atexit
import json
import os

import config
from models import User
from utils import LoadOrInitializeMixin, IDManager, hash_password


class JsonDatabase(LoadOrInitializeMixin):
    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(JsonDatabase, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        super().__init__()
        self.file_dir = 'data/database.json'
        self.id_manager = IDManager()
        self.data = self._load_or_initialize_data()
        self.data_modified = False
        self.set_admin()

        atexit.register(self._exit_handler)

    def _write_data(self):
        if self.data_modified:
            print(f'Saving data to {self.file_dir}')
            with open(self.file_dir, 'w') as file:
                json.dump(self.data, file, indent=4)
            self.data_modified = False

    def is_unique(self, entity_class, entity):

        unique_fields = getattr(entity_class, 'UniqueFields', []) + ['id']

        for field in unique_fields:
            if self.exists(entity_class, **{field: entity.__dict__[field]}):
                print(f'{field} must be unique')
                return False
        return True

    def save(self, entity):

        entity_class = entity.__class__.__name__
        if entity_class not in self.data:
            self.data[entity_class] = {}

        entity_id = self.id_manager.get_id(entity_class)
        entity.__dict__['id'] = entity_id

        if not self.is_unique(entity.__class__, entity):
            return False
        self.data[entity_class][entity_id] = entity.__dict__
        self.data_modified = True
        return True

    def get(self, entity_class, entity_id):

        class_name = entity_class.__name__
        try:
            return self.data[class_name][entity_id]
        except KeyError:
            print(f'{class_name} with id {entity_id} does not exist')
            return None

    def update(self, entity_class, entity_id, values: dict):

        entity = self.get(entity_class, entity_id)
        if entity:
            for key, value in values.items():
                if key in entity:
                    entity[key] = value
                else:
                    print(f'{key} is not a valid field')
            self.data[entity_class.__name__][entity_id] = entity
            self.data_modified = True
        return entity

    def delete(self, entity_class, entity_id):

        entity = self.get(entity_class, entity_id)
        if entity:
            del self.data[entity_class.__name__][entity_id]
            self.data_modified = True

    def filter(self, entity_class, **kwargs):

        class_name = entity_class.__name__

        return [entity for entity in self.data[class_name].values() if
                all(entity[key] == value for key, value in kwargs.items())]

    def all(self, entity_class):

        class_name = entity_class.__name__

        return [entity for entity in self.data[class_name].values()]

    def exists(self, entity_class, **kwargs):

        return any(self.filter(entity_class, **kwargs))

    def count(self, entity_class):

        class_name = entity_class.__name__
        return len(self.data[class_name]) if self.data[class_name] else 0

    def clear(self):

        self.data = {}
        self.data_modified = True

    def _exit_handler(self):

        self._write_data()

    def set_admin(self):
        if not self.data:
            admin_password = hash_password(config.ADMIN_PASSWORD)
            admin = User(config.ADMIN_USERNAME, admin_password)
            admin.is_admin = True
            self.save(admin)
