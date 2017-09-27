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
            app.logger.info('Debug toolbar configured!!!')
        except TypeError:
            app.logger.error('You must install flask_debugtoolbar')
        except RuntimeError as e:
            app.logger.error(str(e))

    if app.config.get('OPBEAT'):
        try:
            Opbeat(
                app,
                logging=app.config.get('OPBEAT', {}).get('LOGGING', False)
            )
            app.logger.info('opbeat configured!!!')
        except TypeError:
            app.logger.error('You must install opbeat')

    if app.config.get('SENTRY_ENABLED', False):
        try:
            app.sentry = Sentry(app)
            app.logger.info('Sentry configured!!!')
        except TypeError:
            app.logger.error('You must install raven (Sentry)')
