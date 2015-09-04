# coding: utf-8

# TODO load from blueprints

import sys

from flask import Blueprint
from werkzeug.routing import Rule
from quokka.core.app import QuokkaModule
from quokka.core.models import Content
from quokka_themes import Theme
from pymongo.mongo_client import MongoClient

if sys.version_info.major == 3:
    unicode = lambda x: u'{}'.format(x)  # noqa  # flake8: noqa
    basestring = str  # noqa  # flake8: noqa

basetypes = (
    int, str, float, dict, list, tuple,
    Blueprint, QuokkaModule, Theme, Rule, MongoClient,
    basestring, unicode
)


def is_instance(v, cls):
    cls_map = {
        tp.__name__: tp for tp in basetypes
    }
    return isinstance(v, cls_map.get(cls, str))


def get_content(**kwargs):
    try:
        return Content.objects.get(**kwargs)
    except:
        return None


def get_contents(limit=None, order_by="-created_at", **kwargs):
    contents = Content.objects.filter(**kwargs).order_by(order_by)
    if limit:
        contents = contents[:limit]
    return contents


def configure(app):
    app.jinja_env.filters['isinstance'] = is_instance
    app.add_template_global(get_content)
    app.add_template_global(get_contents)
