# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    overholt wsgi module
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from quokka import create_app, create_api

application = DispatcherMiddleware(create_app(), {
    '/api': create_api()
})

if __name__ == "__main__":
    run_simple(
        '0.0.0.0',
        5000,
        application,
        use_reloader=True,
        use_debugger=True
    )
