from tinymongo import TinyMongoClient
from quokka.config import settings

db_system = settings.get('db_system', 'tinydb')

if db_system == 'tinydb':
    connection = TinyMongoClient(settings.get('db_folder', 'databases'))
elif db_system == 'mongo':
    connection = 'TODO: Load Pymongo here'


db_contents = connection[settings.get('db_contents', 'content')]
db_uploads = connection[settings.get('db_uploads', 'uploads')]
db_users = connection[settings.get('db_users', 'users')]

collection_contents = db_contents[
    settings.get('collection_contents', 'contents')]
collection_uploads = db_uploads[settings.get('collection_uploads', 'uploads')]
collection_users = db_users[settings.get('collection_users', 'users')]

