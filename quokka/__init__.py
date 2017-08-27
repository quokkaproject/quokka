"""Quokka CMS!"""

__version__ = '0.3.0'

from quokka.admin import create_admin  # noqa
from quokka.app import QuokkaApp  # noqa
from quokka.core import configure_extensions, configure_extension  # noqa
from quokka.core.flask_dynaconf import configure_dynaconf


admin = create_admin()


def create_app_base(config=None, test=False, admin_instance=None,
                    ext_list=None, **settings):
    """Creates basic app only with extensions provided in ext_list
    useful for testing."""

    app = QuokkaApp('quokka')
    configure_dynaconf(app)
    if config:
        app.config.update(config)

    if test or app.config.get('TESTING'):
        app.testing = True
    if ext_list:
        for ext in ext_list:
            configure_extension(ext, app=app)
    return app


def create_app(config=None, test=False, admin_instance=None, **settings):
    """Creates full app with all extensions loaded"""
    app = create_app_base(
        config=config, test=test, admin_instance=admin_instance, **settings
    )
    configure_extensions(app, admin_instance or admin)
    return app
