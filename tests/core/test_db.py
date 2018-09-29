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

def test_class_QuokkaTinyMongoClient():
    pass


def test_class_QuokkaDB():
    pass


def test_is_equal():
    pass

