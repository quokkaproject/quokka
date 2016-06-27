# coding: utf-8
from flask_cache import Cache

cache = Cache()


def configure(app):
    cache.init_app(app)
