import mock
import click
import itertools
from contextlib import suppress
from copy import deepcopy
from pymongo import MongoClient
from tinydb_serialization import SerializationMiddleware
from tinymongo import TinyMongoClient
from tinymongo.serializers import DateTimeSerializer
from tinymongo.tinymongo import generate_id
from quokka.utils.text import split_all_category_roots
from quokka.core.db import QuokkaTinyMongoClient, QuokkaDB


#######################################################
#pytest - fixtures                                    #
#######################################################
quokka_mongo = QuokkaTinyMongoClient()
quokka_db = QuokkaDB()
mock_collections = {'index': 'index', 'contents': 'contents', 'uploads': 'uploads', 'users': 'users'}

#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_class_quokkatinymongoclient_isinstance():
    assert isinstance(quokka_mongo, QuokkaTinyMongoClient) == True

def test_class_quokkadb_isinstance():
    assert isinstance(quokka_db, QuokkaDB) == True

def test_class_quokkadb_collections():
    assert quokka_db.collections == mock_collections

def test_class_quokkadb_config():
    assert quokka_db.config == {}

def test_class_quokkadb_folder():
    assert quokka_db.folder == 'databases'

def test_class_quokkadb_host():
    assert quokka_db.host == 'localhost'

def test_class_quokkadb_name():
    assert quokka_db.name == 'quokka_db'

