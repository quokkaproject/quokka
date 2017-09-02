# coding: utf-8
"""This core extension cannot be loaded from settings.yml
should be loaded directly in create_app"""

from dynaconf.contrib import FlaskDynaconf
from dynaconf.loaders import yaml_loader


def configure_dynaconf(app):
    settings_file = 'quokka.yml'
    initial_envmode = app.config.get('ENVMODE')

    # Extension is supposed to override envmode
    FlaskDynaconf(
        app,
        ENVVAR_FOR_DYNACONF="QUOKKA_SETTINGS_MODULE",
        DYNACONF_NAMESPACE='QUOKKA',
        SETTINGS_MODULE_FOR_DYNACONF=settings_file,
        # extra yaml file override values on settings.yml
        # secrets file is a hidden file and must be excluded on .gitignore
        # all password, token and other sensitive must go there
        # or exported as env var ex: QUOKKA_SECRET_KEY=12345
        YAML='.secrets.yml'
    )

    # Configure extra environment
    envmode = initial_envmode or app.config.get('ENVMODE')
    if envmode is not None:
        yaml_loader.load(
            obj=app.config,
            namespace=envmode,
            filename=settings_file
        )
