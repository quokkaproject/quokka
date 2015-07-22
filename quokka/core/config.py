import os
import collections
from flask.config import Config
from quokka.utils import parse_conf_data


class QuokkaConfig(collections.MutableMapping, Config):
    """A Config object for Flask that tries to ger vars from
    database and then from Config itself"""

    def __init__(self, root_path, defaults=None, *args, **kwargs):
        self.root_path = root_path
        self.store = dict(defaults or {})
        self.update(dict(*args, **kwargs))

    def get_settings_from_db(self, group='settings'):
        try:
            from quokka.core.models import Config
            return {
                item.name: item.value
                for item in Config.objects.get(group=group).values
            }
        except:
            return {}

    def __getitem__(self, key):
        settings = self.get_settings_from_db()
        return settings.get(key) or self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return self.store.__repr__()

    def __unicode__(self):
        return unicode(repr(self.store))

    def __call__(self, *args, **kwargs):
        return self.store.get(*args, **kwargs)

    def __cmp__(self, dict):
        return cmp(self.store, dict)

    def __contains__(self, item):
        return item in self.store

    def copy(self):
        return self.store.copy()

    def keys(self):
        return self.store.keys()

    def values(self):
        return self.store.values()

    def add(self, key, value):
        self.store[key] = value

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
                for key, data in os.environ.items() if key.startswith('QUOKKA')
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
