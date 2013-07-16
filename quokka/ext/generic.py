# coding: utf-8


def configure(app):
    if app.config.get('GRAVATAR'):
        from flask.ext.gravatar import Gravatar
        Gravatar(app, **app.config.get('GRAVATAR'))
