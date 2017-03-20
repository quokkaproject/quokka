# from datetime import datetime
from quokka.config import settings
from tinymongo import TinyMongoClient
from tinydb_serialization import SerializationMiddleware
from tinymongo.serializers import DateTimeSerializer

db_system = settings.get('db_system', 'tinydb')


class QuokkaTinyMongoClient(TinyMongoClient):
    @property
    def _storage(self):
        serialization = SerializationMiddleware()
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
        # TODO: Read custom serializers from settings and extensions
        return serialization


if db_system == 'tinydb':
    connection = QuokkaTinyMongoClient(settings.get('db_folder', 'databases'))
elif db_system == 'mongo':
    connection = 'TODO: Load Pymongo here'


db_index = connection[settings.get('db_index', 'index')]
db_contents = connection[settings.get('db_contents', 'contents')]
db_uploads = connection[settings.get('db_uploads', 'uploads')]
db_users = connection[settings.get('db_users', 'users')]

collection_index = db_index[settings.get('collection_index', 'index')]
collection_contents = db_contents[
    settings.get('collection_contents', 'contents')]
collection_uploads = db_uploads[settings.get('collection_uploads', 'uploads')]
collection_users = db_users[settings.get('collection_users', 'users')]
