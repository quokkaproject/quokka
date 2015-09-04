import os
from flask.config import Config
from quokka.utils import parse_conf_data
from cached_property import cached_property_ttl, cached_property


class QuokkaConfig(Config):
    """A Config object for Flask that tries to ger vars from
    database and then from Config itself"""

    @cached_property
    def store(self):
        return dict(self)

    @cached_property_ttl(300)
    def all_setings_from_db(self):
        """
        As config reads data from database on every app.config.get(key)/[key]
        This data is cached as a cached_property
        The TTL is fixed in 5 minutes because we can't read it from
        config itself.

        Find a way to set the config parameter in a file
        maybe in a config_setting.ini
        It takes 5 minutes for new values to be available
        and Make it possible to use REDIS as a cache
        """
        try:
            from quokka.core.models import Config
            return {
                item.name: item.value
                for item in Config.objects.get(group='settings').values
            }
        except:
            return {}

    def get_from_db(self, key, default=None):
        return self.all_setings_from_db.get(key, default)

    def __getitem__(self, key):
        return self.get_from_db(key) or dict.__getitem__(self, key)

    # def __iter__(self):
    #     return iter(self.store)

    # def __len__(self):
    #     return len(self.store)

    # def __repr__(self):
    #     return self.store.__repr__()

    # def __unicode__(self):
    #     return unicode(repr(self.store))

    # def __call__(self, *args, **kwargs):
    #     return self.store.get(*args, **kwargs)

    # def __contains__(self, item):
    #     return item in self.store

    # def keys(self):
    #     return self.store.keys()

    # def values(self):
    #     return self.store.values()

    def get(self, key, default=None):
        return self.get_from_db(key) or self.store.get(key) or default

    def from_object(self, obj, silent=False):
        try:
            super(QuokkaConfig, self).from_object(obj)
        except ImportError as e:
            if silent:
                return False
            e.message = 'Unable to load configuration obj (%s)' % e.message
            raise

    def from_envvar_namespace(self, namespace='QUOKKA', silent=False):
        try:
            data = {
                key.partition('_')[-1]: parse_conf_data(data)
                for key, data
                in os.environ.items()
                if key.startswith(namespace)
            }
            self.update(data)
        except Exception as e:
            if silent:
                return False
            e.message = 'Unable to load config env namespace (%s)' % e.message
            raise

    def load_quokka_config(self, config=None, mode=None, test=None, **sets):
        self.from_object(config or 'quokka.settings')
        mode = mode or 'test' if test else os.environ.get(
            'QUOKKA_MODE', 'local')
        self.from_object('quokka.%s_settings' % mode, silent=True)
        path = "QUOKKA_SETTINGS" if not test else "QUOKKATEST_SETTINGS"
        self.from_envvar(path, silent=True)
        self.from_envvar_namespace(namespace='QUOKKA', silent=True)
        self.update(sets)
