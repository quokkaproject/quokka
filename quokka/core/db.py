import itertools
from contextlib import suppress
from copy import deepcopy

from pymongo import MongoClient
from tinydb_serialization import SerializationMiddleware
from tinymongo import TinyMongoClient
from tinymongo.serializers import DateTimeSerializer
from tinymongo.tinymongo import generate_id

from quokka.utils.text import split_all_category_roots


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
        """Get the corresponding database collection/table"""
        col_name = self.collections.get(collection, collection)
        db_name = self.get_db_name(col_name)
        return self.connection[db_name][col_name]

    def get_content_collection(self, content_id):
        return self.connection[content_id]['contents']

    def get_content_collection_mongo(self, content_id):
        return self.connection[self.name]['contents']

    @property
    def connection(self):
        if getattr(self, '_connection', None) is None:
            if self.system == 'tinydb':
                self._connection = QuokkaTinyMongoClient(self.folder)
            elif self.system == 'mongo':
                self._connection = MongoClient(
                    host=self.host,
                    port=self.port
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

    def generate_id(self):
        return generate_id()

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

    def author_set(self, sort=True, **kwargs):
        users = [
            item.get('fullname', item.get('username'))
            for item in self.users.find()
        ]
        authors = self.value_set('index', 'authors', flat=True, **kwargs)
        values = list(set(users + authors))
        return sorted(values) if sort is True else values

    def tag_set(self, sort=True, **kwargs):
        return self.value_set('index', 'tags', flat=True, sort=sort, **kwargs)

    def category_set(self, sort=True, **kwargs):
        results = self.value_set('index', 'category', sort=sort, **kwargs)
        cats = []
        for result in results:
            cats.extend(split_all_category_roots(result))
        return sorted(set(cats)) if sort is True else set(cats)

    def content_set(self, *args, **kwargs):
        return self.index.find(*args, **kwargs)

    def article_set(self, *args, **kwargs):
        kwargs.setdefault(
            'sort',
            self.app.theme_context.get('ARTICLE_ORDER_BY', [('date', -1)])
        )
        if not args:
            args = [{'content_type': 'article'}]
        elif isinstance(args[0], dict):
            args[0]['content_type'] = 'article'
        return self.content_set(*args, **kwargs)

    def page_set(self, *args, **kwargs):
        kwargs.setdefault(
            'sort',
            self.app.theme_context.get('PAGE_ORDER_BY', [('title', -1)])
        )
        if not args:
            args = [{'content_type': 'page'}]
        elif isinstance(args[0], dict):
            args[0]['content_type'] = 'page'
        return self.content_set(*args, **kwargs)

    def block_set(self, *args, **kwargs):
            kwargs.setdefault(
                'sort',
                self.app.theme_context.get(
                    'BLOCK_ORDER_BY', [('title', -1)]
                )
            )
            if not args:
                args = [{'content_type': 'block'}]
            elif isinstance(args[0], dict):
                args[0]['content_type'] = 'block'
            return self.content_set(*args, **kwargs)

    def select(self, colname, *args, **kwargs):
        return self.get_collection(colname).find(*args, **kwargs)

    def count(self, colname, *args, **kwargs):
        return self.get_collection(colname).find(*args, **kwargs).count()

    def get(self, colname, *args, **kwargs):
        return self.get_collection(colname).find_one(*args, **kwargs)

    def insert(self, colname, *args, **kwargs):
        return self.get_collection(colname).insert(*args, **kwargs)

    def push_content(self, model):
        """Insert or Update content related to model"""
        collection = self.get_content_collection(model['_id'])
        current_saved = collection.find_one({
            'content_id': model['_id'],
            'version': model.get('version', 0)
        })

        if is_equal(model, current_saved):
            model.pop('content', None)
            return

        model_to_save = deepcopy(model)

        if not current_saved:
            version = 0
        else:
            version = model.get('version', 0) + 1

        model['version'] = model_to_save['version'] = version

        model_to_save['content_id'] = model_to_save.pop('_id')
        collection.insert(model_to_save)
        model.pop('content', None)

    def pull_content(self, model):
        if not isinstance(model, dict):
            model = self.get('index', {'_id': model})

        if not model or (
                model.get('version') == 0 and not model.get('_isclone')):
            return

        collection = self.get_content_collection(model['_id'])
        record = collection.find_one({
            'content_id': model['_id'],
            'version': model['version']
        })
        return record['content'] if record else None

    def get_with_content(self, **kwargs):
        model = self.get('index', kwargs)
        if model:
            model['content'] = self.pull_content(model)
        return model


def is_equal(model, other):
    if not other:
        return False

    versioned_keys = [
        'title', 'summary', 'tags', 'category', 'date',
        'content', 'authors', 'slug', 'status', 'published',
        'comments', 'block_items'
    ]
    for key in versioned_keys:
        if model.get(key) != other.get(key):
            return False

    return True
