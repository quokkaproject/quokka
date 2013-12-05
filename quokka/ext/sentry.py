# coding: utf-8


def configure(app):
    from raven.contrib.flask import Sentry
    app.sentry = Sentry(app)
