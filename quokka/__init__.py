#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERSION = (0, 2, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "Alpha"
__description__ = "Flexible & modular CMS powered by Flask and MongoDB"
__author__ = "Bruno Rocha <rochacbruno@gmail.com>"
__email__ = "quokka-developers@googlegroups.com"
__license__ = "MIT License"
__copyright__ = "Copyright 2013, Quokka Project / PythonHub.com"

import os
from .core.admin import create_admin
from .core.app import QuokkaApp
# from .core.middleware import HTTPMethodOverrideMiddleware


admin = create_admin()


def create_app(config=None, test=False, admin_instance=None, **settings):
    app = QuokkaApp('quokka')
    app.config.from_object(config or 'quokka.settings')
    mode = os.environ.get('MODE', 'local')
    if test:
        mode = 'test'
    try:
        app.config.from_object('quokka.%s_settings' % mode)
    except ImportError:
        pass

    app.config.update(settings)

    if not test:
        app.config.from_envvar("QUOKKA_SETTINGS", silent=True)
    else:
        app.config.from_envvar("QUOKKATEST_SETTINGS", silent=True)

    from .ext import configure_extensions
    configure_extensions(app, admin_instance or admin)

    # app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    return app


def create_api(config=None, **settings):
    return None


def create_celery_app(app=None):
    from celery import Celery
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
