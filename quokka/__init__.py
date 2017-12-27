"""Quokka CMS!"""

__version__ = '0.3.4'

from pathlib import Path
from quokka.core.app import QuokkaApp
from quokka.core import configure_extensions, configure_extension
from quokka.core.flask_dynaconf import configure_dynaconf


def create_app_base(test=False, ext_list=None, **settings):
    """Creates basic app only with extensions provided in ext_list
    useful for testing."""

    app = QuokkaApp('quokka')
    if settings:
        app.config.update(settings)
    configure_dynaconf(app)

    if test or app.config.get('TESTING'):
        app.testing = True

    app.static_folder = Path.cwd() / Path('static')
    # Path(app.config['PROJECT_ROOT'])

    if ext_list:
        for ext in ext_list:
            configure_extension(ext, app=app)

    return app


def create_app(test=False, **settings):
    """Creates full app with all extensions loaded"""
    app = create_app_base(test=test, **settings)
    configure_extensions(app)
    return app
