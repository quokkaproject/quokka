#coding: utf-8
from flask import request
from flask.ext.babel import Babel

babel = Babel()


def configure(app):
    babel.init_app(app)

    def get_locale():
        return request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES'])
    babel.localeselector(get_locale)
