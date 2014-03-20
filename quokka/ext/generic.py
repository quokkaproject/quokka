# coding: utf-8

from flask.ext.mistune import Mistune
from flask_wtf.csrf import CsrfProtect


def configure(app):
    # Markdown(app)
    Mistune(app)
    CsrfProtect(app)
    if app.config.get('GRAVATAR'):
        from flask.ext.gravatar import Gravatar
        Gravatar(app, **app.config.get('GRAVATAR'))
