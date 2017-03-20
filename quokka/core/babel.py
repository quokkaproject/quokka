# coding: utf-8
from flask import request, session
from flask_babelex import Babel

babel = Babel()


def configure(app):
    babel.init_app(app)

    if babel.locale_selector_func is None:
        @babel.localeselector
        def get_locale():
            override = request.args.get('lang')
            if override:
                session['lang'] = override
            else:
                # use default language if set
                if app.config.get('BABEL_DEFAULT_LOCALE'):
                    session['lang'] = app.config.get('BABEL_DEFAULT_LOCALE')
                else:
                    # get best matching language
                    if app.config.get('BABEL_LANGUAGES'):
                        session['lang'] = request.accept_languages.best_match(
                            app.config.get('BABEL_LANGUAGES')
                        )

            return session.get('lang', 'en')

        # @babel.localeselector
        # def get_locale():
        #     if request.args.get('lang'):
        #         session['lang'] = request.args.get('lang')
        #     return session.get('lang', 'en')
