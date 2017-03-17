# coding: utf-8

from flask_mistune import Mistune


def configure(app):
    Mistune(app)
