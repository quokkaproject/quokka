# coding: utf-8

# TODO load from blueprints

basetypes = (int, str, float, unicode, basestring, dict, list, tuple)


def is_instance(v, cls):
    cls_map = {
        tp.__name__: tp for tp in basetypes
    }
    return isinstance(v, cls_map.get(cls, str))


def configure(app):
    app.jinja_env.filters['isinstance'] = is_instance
