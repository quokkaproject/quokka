# coding: utf-8


def configure(app, admin=None):
    if app.config.get('DEBUG_TOOLBAR_ENABLED'):
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            DebugToolbarExtension(app)
        except ImportError:
            app.logger.info('flask_debugtoolbar is not installed')

    if app.config.get('OPBEAT'):
        try:
            from opbeat.contrib.flask import Opbeat
            Opbeat(
                app,
                logging=app.config.get('OPBEAT', {}).get('LOGGING', False)
            )
            app.logger.info('opbeat configured!!!')
        except ImportError:
            app.logger.info('opbeat is not installed')

    if app.config.get('SENTRY_ENABLED', False):
        try:
            from raven.contrib.flask import Sentry
            app.sentry = Sentry(app)
        except ImportError:
            app.logger.info('sentry, raven is not installed')
