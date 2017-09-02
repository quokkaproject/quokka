# coding: utf-8
from inspect import getargspec
import sys
import import_string


def configure_extension(name, **kwargs):
    configurator = import_string(name)
    args = getargspec(configurator).args
    configurator(**{key: val for key, val in kwargs.items() if key in args})


def configure_extensions(app, admin=None):
    """Configure extensions provided in config file"""
    sys.path.insert(0, './modules')
    extensions = app.config.get(
        'CORE_EXTENSIONS', []
    ) + app.config.get(
        'EXTRA_EXTENSIONS', []
    )
    for configurator_name in extensions:
        configure_extension(configurator_name, app=app, admin=admin)
    return app
