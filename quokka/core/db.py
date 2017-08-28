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


class QuokkaDB:
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.config = app.config.get('DATABASE', {})
        self.system = self.config.get('system', 'tinydb')
        self.folder = self.config.get('folder', 'databases')
        self.username = self.config.get('username')
        self.password = self.config.get('password')
        self.host = self.config.get('host', 'localhost')
        self.port = self.config.get('port', 'port')
        self.name = self.config.get('name', 'quokka_db')
        self.collections = {
            'index': 'index',
            'contents': 'contents',
            'uploads': 'uploads',
            'users': 'users',
        }
        self.collections.update(self.config.get('collections', {}))
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
        col_name = self.collections[collection]
        db_name = self.get_db_name(col_name)
        return self.connection[db_name][col_name]

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

    @property
    def index(self):
        return self.get_collection('index')

    @property
    def contents(self):
        return self.get_collection('contents')

    @property
    def uploads(self):
        return self.get_collection('uploads')

    @property
    def users(self):
        return self.get_collection('users')
