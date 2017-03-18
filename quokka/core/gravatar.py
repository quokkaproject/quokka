# coding: utf-8

try:
    from flask_gravatar import Gravatar
except ImportError:
    Gravatar = None


def configure(app):
    if app.config.get('GRAVATAR'):
        try:
            Gravatar(app, **app.config.get('GRAVATAR'))
        except TypeError:
            raise ImportError('You must install flask_gravatar')
