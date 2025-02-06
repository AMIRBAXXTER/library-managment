import json
import os


class IDManager:
    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(IDManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        self.file_dir = 'data/ids.json'
        self._initialize_ids()
        self.ids = {}
        self._load_ids()

    def _initialize_ids(self):

        if not os.path.exists(self.file_dir):
            os.makedirs(os.path.dirname(self.file_dir), exist_ok=True)
            with open(self.file_dir, 'w') as file:
                json.dump({}, file)

    def _load_ids(self):

        with open(self.file_dir, 'r') as file:
            self.ids = json.load(file)

    def _write_ids(self):

        with open(self.file_dir, 'w') as file:
            json.dump(self.ids, file, indent=4)

    def get_id(self, entity_class):

        if entity_class not in self.ids:
            self.ids[entity_class] = 0
        self.ids[entity_class] += 1
        self._write_ids()
        return self.ids[entity_class]


class JsonDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(JsonDatabase, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        self.file_dir = 'data/database.json'
        self._initialize_database()
        self.id_manager = IDManager()
        self.data = {}
        self._load_data()

    def _initialize_database(self):

        if not os.path.exists(self.file_dir):
            os.makedirs(os.path.dirname(self.file_dir), exist_ok=True)
            with open(self.file_dir, 'w') as file:
                json.dump({}, file)

    def _load_data(self):

        with open(self.file_dir, 'r') as file:
            self.data = json.load(file)

    def _write_data(self):

        with open(self.file_dir, 'w') as file:
            json.dump(self.data, file, indent=4)

    def is_unique(self, entity_class, entity):
        if hasattr(entity_class, 'UniqueFields'):
            unique_fields = [field for field in entity.__class__.UniqueFields or []] + ['id']
        else:
            unique_fields = ['id']

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
            return
        self.data[entity_class][entity_id] = entity.__dict__
        self._write_data()

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
            self._write_data()

    def delete(self, entity_class, entity_id):

        entity = self.get(entity_class, entity_id)
        if entity:
            del self.data[entity_class.__name__][entity_id]
            self._write_data()

    def filter(self, entity_class, **kwargs):

        class_name = entity_class.__name__
        if class_name not in self.data:
            return []
        return [entity for entity in self.data[class_name].values() if
                all(entity[key] == value for key, value in kwargs.items())]

    def all(self, entity_class):

        class_name = entity_class.__name__
        if class_name not in self.data:
            return []
        return [entity for entity in self.data[class_name].values()]

    def exists(self, entity_class, **kwargs):

        return len(self.filter(entity_class, **kwargs)) > 0

    def count(self, entity_class):

        class_name = entity_class.__name__
        return len(self.data[class_name]) if self.data[class_name] else 0

    def clear(self):

        self.data = {}
        self._write_data()
