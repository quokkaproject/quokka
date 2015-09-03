from flask import current_app, request
from quokka.core.db import db
from quokka.core.app import QuokkaApp


def create_app_min(config=None, test=False):
    app = QuokkaApp('quokka')
    app.config.load_quokka_config(config=config, test=test)
    return app


def get_site_url():
    from quokka.core.models import Config
    try:
        from_site_config = Config.get('site', 'site_domain', None)
        from_settings = get_setting_value('SERVER_NAME', None)
        if from_settings and not from_settings.startswith('http'):
            from_settings = 'http://%s/' % from_settings
        return from_site_config or from_settings or request.url_root
    except RuntimeError:
        return 'http://localhost/'


def get_setting_value(key, default=None):
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
