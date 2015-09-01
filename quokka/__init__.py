#!/usr/bin/env python
# -*- coding: utf-8 -*-
VERSION = (0, 2, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "Alpha"
__description__ = "Flexible & modular CMS powered by Flask and MongoDB"
__author__ = "Bruno Rocha <rochacbruno@gmail.com>"
__email__ = "quokka-developers@googlegroups.com"
__license__ = "MIT License"
__copyright__ = "Copyright 2014, Quokka Project"


try:
    from .core.admin import create_admin
    from .core.app import QuokkaApp
    # from .core.middleware import HTTPMethodOverrideMiddleware
    admin = create_admin()
except:
    pass


def create_app_base(config=None, test=False, admin_instance=None, **settings):
    app = QuokkaApp('quokka')
    app.config.load_quokka_config(config=config, test=test, **settings)
    if test or app.config.get('TESTING'):
        app.testing = True
    return app


def create_app(config=None, test=False, admin_instance=None, **settings):
    app = create_app_base(
        config=config, test=test, admin_instance=admin_instance, **settings
    )
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
    taskbase = celery.Task

    class ContextTask(taskbase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return taskbase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
