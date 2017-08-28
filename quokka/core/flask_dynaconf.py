# coding: utf-8
"""This core extension cannot be loaded from settings.yml
should be loaded directly in create_app"""

from dynaconf.contrib import FlaskDynaconf
# from quokka.config import settings


def configure_dynaconf(app):
    FlaskDynaconf(
        app,
        ENVVAR_FOR_DYNACONF="QUOKKA_SETTINGS_MODULE",
        DYNACONF_NAMESPACE='QUOKKA',
        SETTINGS_MODULE_FOR_DYNACONF='settings.yml',
        YAML='.secrets.yml'  # extra yaml file override ^
    )
