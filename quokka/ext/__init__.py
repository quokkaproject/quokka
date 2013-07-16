# coding: utf-8
from flask.ext.mail import Mail
from flask.ext.cache import Cache
from dealer.contrib.flask import Dealer

from . import generic, babel


def configure_extensions(app):
    babel.configure(app)
    generic.configure(app)
    Cache(app)
    Mail(app)
    Dealer(app)
    return app
