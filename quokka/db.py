from tinymongo import TinyMongoClient


connection = TinyMongoClient('databases')
db = connection['quokka_db']
