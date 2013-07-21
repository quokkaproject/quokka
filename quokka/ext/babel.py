#coding: utf-8
# from flask import request, session
from flask.ext.babelex import Babel

babel = Babel()


def configure(app):
    babel.init_app(app)

    # @babel.localeselector
    # def get_locale():
    #     override = request.args.get('lang')

    #     if override:
    #         session['lang'] = override

    #     return session.get('lang', 'en')

    # def get_locale():
    #     return request.accept_languages.best_match(
    #         app.config['BABEL_LANGUAGES'])
    # babel.localeselector(get_locale)
