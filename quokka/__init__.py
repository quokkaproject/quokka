#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERSION = (0, 1, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Flexible & modular CMS powered by Flask and MongoDB"
__author__ = u"Bruno Rocha"
__credits__ = []
__email__ = u"quokka-developers@googlegroups.com"
__license__ = u"MIT License"
__copyright__ = u"Copyright 2013, Quokka Project"

import os
from flask import Flask
from core.admin import create_admin
# from quokka.core.middleware import HTTPMethodOverrideMiddleware


admin = create_admin()


def create_app(config=None, test=False, admin_instance=None, **settings):
    app = Flask('quokka')
    app.config.from_envvar("APP_SETTINGS", silent=True)
    app.config.from_object(config or 'quokka.settings')

    # Settings from mode
    mode = os.environ.get('MODE')
    if mode:
        app.config.from_object('base.config.%s' % mode)

    # Local settings
    if not test:
        app.config.from_pyfile(
            os.path.join(os.path.dirname(__file__), 'local_settings.py'),
            silent=True
        )

    # Overide settings
    app.config.update(settings)

    # with app.test_request_context():
    from ext import configure_extensions
    configure_extensions(app, admin_instance or admin)

    # app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    return app


def create_api(config=None, **settings):
    return None


def create_celery_app(app=None):
    from celery import Celery
    app = app or create_app('quokka', os.path.dirname(__file__))
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
