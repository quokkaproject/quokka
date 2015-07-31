# coding: utf-8

from shiftpy.wsgi_utils import envify


def activate(app):
    # If running on Openshift wraps its virtualenv, otherwise do nothing
    envify(app)
    # Space left to insert hooks to another PaaS if needed
    return app
