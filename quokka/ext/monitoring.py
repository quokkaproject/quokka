# coding: utf-8

try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError:
    DebugToolbarExtension = None

try:
    from opbeat.contrib.flask import Opbeat
except ImportError:
    Opbeat = None

try:
    from raven.contrib.flask import Sentry
except ImportError:
    Sentry = None


def configure(app, admin=None):
    if app.config.get('DEBUG_TOOLBAR_ENABLED'):
        try:
            DebugToolbarExtension(app)
        except TypeError:
            raise ImportError('You must install flask_debugtoolbar')

    if app.config.get('OPBEAT'):
        try:
            Opbeat(
                app,
                logging=app.config.get('OPBEAT', {}).get('LOGGING', False)
            )
            app.logger.info('opbeat configured!!!')
        except TypeError:
            raise ImportError('You must install opbeat')

    if app.config.get('SENTRY_ENABLED', False):
        try:
            app.sentry = Sentry(app)
        except TypeError:
            raise ImportError('You must install raven (Sentry)')
