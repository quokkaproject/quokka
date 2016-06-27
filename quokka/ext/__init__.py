# coding: utf-8
from inspect import getargspec
from werkzeug.utils import import_string
from quokka.core.db import db


def configure_extension(name, **kwargs):
    configurator = import_string(name)
    args = getargspec(configurator).args
    if 'db' in args and 'db' not in kwargs:
        kwargs['db'] = db
    configurator(**{key: val for key, val in kwargs.items() if key in args})


def configure_extensions(app, admin):
    extensions = app.config.get(
        'CORE_EXTENSIONS', []
    ) + app.config.get(
        'EXTRA_EXTENSIONS', []
    )
    for configurator_name in extensions:
        configure_extension(configurator_name, app=app, db=db, admin=admin)
    return app
