# coding: utf-8
from flask.ext.mail import Mail
from flask.ext.security import Security as _Security
from flask.ext.security import MongoEngineUserDatastore

from dealer.contrib.flask import Dealer
from quokka.core.db import db
from quokka.core.cache import cache
from quokka.core.admin import configure_admin
from quokka.core.templates import render_template
from quokka.modules.accounts.models import Role, User

from . import (generic, babel, blueprints, error_handlers, context_processors,
               template_filters, before_request, views, themes, fixtures,
               oauthlib, weasyprint)


class Security(_Security):
    def render_template(self, *args, **kwargs):
        return render_template(*args, **kwargs)


def configure_extensions(app, admin):
    cache.init_app(app)
    babel.configure(app)
    generic.configure(app)
    Mail(app)
    Dealer(app)
    error_handlers.configure(app)
    db.init_app(app)

    themes.configure(app, db)  # Themes should be configured after db

    context_processors.configure(app)
    template_filters.configure(app)

    app.security = Security(app, MongoEngineUserDatastore(db, User, Role))

    fixtures.configure(app, db)
    blueprints.load_from_packages(app)
    blueprints.load_from_folder(app)

    # enable .pdf support for posts
    weasyprint.configure(app)

    configure_admin(app, admin)

    if app.config.get('DEBUG_TOOLBAR_ENABLED'):
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            DebugToolbarExtension(app)
        except:
            pass

    before_request.configure(app)
    views.configure(app)

    oauthlib.configure(app)

    if app.config.get('SENTRY_ENABLED', False):
        from .sentry import configure
        configure(app)

    return app
