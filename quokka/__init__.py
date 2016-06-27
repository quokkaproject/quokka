#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter("ignore", category=ExtDeprecationWarning)
# The above hack is needed because flask_mongoengine and flask_cache
# Did not migrated from old flask.ext style

from quokka.core.admin import create_admin  # noqa
from quokka.core.app import QuokkaApp  # noqa
from quokka.core.middleware import HTTPMethodOverrideMiddleware  # noqa
from quokka.ext import configure_extensions, configure_extension  # noqa

admin = create_admin()


def create_app_base(config=None, test=False, admin_instance=None,
                    ext_list=None, **settings):
    app = QuokkaApp('quokka')
    app.config.load_quokka_config(config=config, test=test, **settings)
    if test or app.config.get('TESTING'):
        app.testing = True
    if ext_list:
        for ext in ext_list:
            configure_extension(ext, app=app)
    return app


def create_app(config=None, test=False, admin_instance=None, **settings):
    app = create_app_base(
        config=config, test=test, admin_instance=admin_instance, **settings
    )

    configure_extensions(app, admin_instance or admin)
    if app.config.get("HTTP_PROXY_METHOD_OVERRIDE"):
        app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
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
