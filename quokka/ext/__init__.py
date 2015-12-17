# coding: utf-8
from flask_mail import Mail
from quokka.core.db import db
from quokka.core.cache import cache
from quokka.core.admin import configure_admin

from . import (generic, babel, blueprints, error_handlers, context_processors,
               template_filters, before_request, views, themes, fixtures,
               oauthlib, weasyprint, security, development)


def configure_extensions(app, admin):
    cache.init_app(app)
    babel.configure(app)
    generic.configure(app)
    Mail(app)
    error_handlers.configure(app)
    db.init_app(app)
    themes.configure(app)
    context_processors.configure(app)
    template_filters.configure(app)
    security.configure(app, db)
    fixtures.configure(app, db)
    # blueprints.load_from_packages(app)
    blueprints.load_from_folder(app)
    weasyprint.configure(app)
    configure_admin(app, admin)
    development.configure(app, admin)
    before_request.configure(app)
    views.configure(app)
    oauthlib.configure(app)
    return app


def configure_extensions_min(app, *args, **kwargs):
    db.init_app(app)
    security.init_app(app, db)
    return app
