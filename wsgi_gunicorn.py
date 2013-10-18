# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from werkzeug.contrib.fixers import ProxyFix
from quokka import create_app

application = create_app()

application.wsgi_app = ProxyFix(application.wsgi_app)

"""
see this post
http://www.onurguzel.com/
how-to-run-flask-applications-with-nginx-using-gunicorn/
"""

if __name__ == "__main__":
    run_simple(
        '0.0.0.0',
        5000,
        application,
        use_reloader=True,
        use_debugger=True
    )
