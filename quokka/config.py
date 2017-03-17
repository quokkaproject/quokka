# coding: utf-8
from flask.config import Config
from dynaconf import LazySettings

settings = LazySettings(
    ENVVAR_FOR_DYNACONF="QUOKKA_SETTINGS_MODULE",
    DYNACONF_NAMESPACE='QUOKKA',
    SETTINGS_MODULE_FOR_DYNACONF='settings.yml'
)


# TODO: extract this as a new extension flask_dynaconf
class DynaconfConfig(Config):
    def get(self, key, default=None):
        """Gets config from dynaconf variables
        if variables does not exists in dynaconf try getting from
        app.config to support runtime settings."""
        return settings.get(key, Config.get(self, key, default))

    def __init__(self, *args, **kwargs):
        """perform the initial load"""
        super(DynaconfConfig, self).__init__(*args, **kwargs)
        Config.update(self, settings.store)

    def __getitem__(self, key):
        return self.get(key)
