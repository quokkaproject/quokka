# coding: utf-8
"""This core extension cannot be loaded from settings.yml
should be loaded directly in create_app"""

from dynaconf.contrib import FlaskDynaconf
from quokka.config import settings


def configure_dynaconf(app):
    FlaskDynaconf(app, dynaconf_instance=settings)
