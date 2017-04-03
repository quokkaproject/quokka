# coding: utf-8
from flask import Flask, Blueprint
from flask.helpers import _endpoint_from_view_func


class QuokkaApp(Flask):
    """
    Implementes customizations on Flask
    - custom add_quokka_url_rule
    """

    def add_quokka_url_rule(self, rule, endpoint=None,
                            view_func=None, **options):
        """Builds urls using quokka. prefix to avoid conflicts
        with external modules urls."""
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        if not endpoint.startswith('quokka.'):
            endpoint = 'quokka.' + endpoint
        self.add_url_rule(rule, endpoint, view_func, **options)


class QuokkaModule(Blueprint):
    """Overwrite blueprint namespace to quokka.modules.name
    to avoid conflicts with external Blueprints use same name"""

    def __init__(self, name, *args, **kwargs):
        name = "quokka.modules." + name
        super(QuokkaModule, self).__init__(name, *args, **kwargs)
