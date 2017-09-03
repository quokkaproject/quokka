import itertools
from contextlib import suppress

from pymongo import MongoClient
from tinydb_serialization import SerializationMiddleware
from tinymongo import TinyMongoClient
from tinymongo.serializers import DateTimeSerializer


class QuokkaTinyMongoClient(TinyMongoClient):
    @property
    def _storage(self):
        serialization = SerializationMiddleware()
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
        # TODO: Read custom serializers from settings and extensions
        return serialization


class QuokkaDB(object):

    config = {}
    system = 'tinydb'
    folder = 'databases'
    username = None
    password = None
    host = 'localhost'
    port = 27017
    name = 'quokka_db'
    collections = {
        'index': 'index',
        'contents': 'contents',
        'uploads': 'uploads',
        'users': 'users',
    }

    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.config = app.config.get('DATABASE', {})

        # update atributes with config counterparts
        for key, value in self.config.items():
            if key.lower() != 'collections':
                setattr(self, key.lower(), value)
            else:
                self.collections.update(value)

        self._register(app)

    def _register(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if 'db' in app.extensions:
            raise RuntimeError("Flask extension already initialized")

        app.extensions['db'] = self
        self.app = app

    def get_db_name(self, collection):
        """return db_name for collection"""
        if self.system == "mongo":
            return self.name
        return collection

    def get_collection(self, collection):
        col_name = self.collections.get(collection, collection)
        db_name = self.get_db_name(col_name)
        return self.connection[db_name][col_name]

    def get_content_collection(self, content_id, page='page1'):
        return self.connection[content_id][page]

    def get_content_collection_mongo(self, content_id, page='page1'):
        return self.get_collection('contents')

    @property
    def connection(self):
        if getattr(self, '_connection', None) is None:
            if self.system == 'tinydb':
                self._connection = QuokkaTinyMongoClient(self.folder)
            elif self.system == 'mongo':
                self._connection = MongoClient(
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password
                )
        return self._connection

    def __dir__(self):
        """Return existing attributes + collection names"""
        attrs = []
        for attr in super().__dir__():
            if attr.endswith(('_mongo', '_tinydb')):
                attrs.append(attr.rpartition('_')[0])
            else:
                attrs.append(attr)
        return sorted(list(set(attrs)) + list(self.collections.keys()))

    def __getattribute__(self, name):
        collections = super().__getattribute__('collections')
        get_collection = super().__getattribute__('get_collection')
        if name in collections:
            return get_collection(name)

        # Try to get system specific method e.g: self.categories_mongo
        try:
            system = super().__getattribute__('system')
            return super().__getattribute__(f'{name}_{system}')
        except AttributeError:
            return super().__getattribute__(name)

    # [ <-- DB query helpers --> ]

    def value_set(self, colname, key, filter=None,
                  sort=True, flat=False, **kwargs):
        """Return a set of all values in a key"""
        if filter is not None:
            data = self.get_collection(colname).find(filter, **kwargs)
        else:
            data = self.get_collection(colname).find(**kwargs)

        values = [item.get(key) for item in data if item.get(key) is not None]

        if flat is True:
            values = list(itertools.chain(*values))

        with suppress(TypeError):
            values = list(set(values))

        return sorted(values) if sort is True else values

    def author_set(self, sort=True):
        users = [
            item.get('fullname', item.get('username'))
            for item in self.users.find()
        ]
        authors = self.value_set('index', 'authors', flat=True)
        values = list(set(users + authors))
        return sorted(values) if sort is True else values

    def content_set(self, *args, **kwargs):
        return self.index.find(*args, **kwargs)

    def select(self, colname, *args, **kwargs):
        return self.get_collection(colname).find(*args, **kwargs)

    def count(self, colname, *args, **kwargs):
        return self.get_collection(colname).find(*args, **kwargs).count()

    def get(self, colname, *args, **kwargs):
        return self.get_collection(colname).find_one(*args, **kwargs)

    def insert(self, colname, *args, **kwargs):
        return self.get_collection(colname).insert(*args, **kwargs)

    def upsert_content(self, model):
        """Insert or Update content related to model"""
        model_content = model.pop('content', None)
        if model_content is None:
            # todo: check existing content and clean it
            return

        content = {
          '_id': model['_id'],  # use the same model_id
          'content_type': model['content_type'],
          'content': model_content
          # TODO: add more metadata
        }
        col = self.get_content_collection(model['_id'])
        # versioning ...
