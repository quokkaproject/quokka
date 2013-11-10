# coding: utf-8

# TODO load from blueprints

from flask import Blueprint
from werkzeug.routing import Rule
from quokka.core.app import QuokkaModule
from quokka_themes import Theme


basetypes = (int, str, float, unicode, basestring, dict, list, tuple,
             Blueprint, QuokkaModule, Theme, Rule)


def is_instance(v, cls):
    cls_map = {
        tp.__name__: tp for tp in basetypes
    }
    return isinstance(v, cls_map.get(cls, str))


def configure(app):
    app.jinja_env.filters['isinstance'] = is_instance
