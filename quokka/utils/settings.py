import os
from flask import current_app
from quokka.core.db import db
from quokka.core.app import QuokkaApp


def create_app_min(config=None, test=False):
    app = QuokkaApp('quokka')
    app.config.from_object(config or 'quokka.settings')
    mode = os.environ.get('QUOKKA_MODE', 'local')
    app.config.from_object('quokka.%s_settings' % mode, silent=True)
    path_settings = "QUOKKA_SETTINGS" if not test else "QUOKKATEST_SETTINGS"
    app.config.from_envvar(path_settings, silent=True)
    app.config.from_envvar_namespace(namespace='QUOKKA', silent=True)
    return app


def get_setting_value(key, default=None):
    """
    # TODO: it is not reading setting from db on models
    """

    try:
        return current_app.config.get(key, default)
    except RuntimeError:
        pass
        
    try:
        app = create_app_min()
        db.init_app(app)
        with app.app_context():
            return app.config.get(key, default)
    except:
        return default


def get_password(f):
    try:
        return open('.%s_password.txt' % f).read().strip()
    except:
        return
