# coding: utf-8

# import datetime
from flask import Markup
from dynaconf.loaders import yaml_loader, env_loader


def configure(app):

    # add context processors
    @app.context_processor
    def app_theme_context():
        context = {
            'JINJA_ENVIRONMENT': app.jinja_env,
            'DEFAULT_LANG': app.config.get('BABEL_DEFAULT_LOCALE'),
            'default_locale': app.config.get('BABEL_DEFAULT_LOCALE'),
            'PAGES': [],
            'pages': [],
            'articles': [],
            'categories': [],
            # https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud
            'tag_cloud': [],
            'JINJA_EXTENSIONS': app.jinja_env.extensions,
            'USE_LESS': False,
            'SITEURL': '',
            'THEME_STATIC_DIR': 'theme',
            'FAVICON': 'favicon.ico',
            'FAVICON_IE': 'favicon.ico',
            'AVATAR': 'LOAD FROM UPLOADS'
        }

        # load theme variables from YAML file
        yaml_loader.load(
            obj=context,
            namespace='theme',
            filename=app.config.get('SETTINGS_MODULE')
        )
        # overrride with QUOKKA_THEME_ prefixed env vars if exist
        env_loader.load_from_env(
            identifier='theme',
            key=None,
            namespace='quokka_theme',
            obj=context,
            silent=True
        )
        # load theme specific variables from YAML
        yaml_loader.load(
            obj=context,
            namespace=f'theme_{app.config.get("THEME_ACTIVE")}',
            filename=app.config.get('SETTINGS_MODULE')
        )
        # overrride with QUOKKA_THEME_THEMENAME prefixed env vars if exist
        env_loader.load_from_env(
            identifier=f'theme_{app.config.get("THEME_ACTIVE")}',
            key=None,
            namespace=f'quokka_theme_{app.config.get("THEME_ACTIVE")}',
            obj=context,
            silent=True
        )

        # TODO: LOAD THEME VARS FROM MODEL

        # mark strings as safe Markup
        for k, v in context.items():
            if isinstance(v, str):
                context[k] = Markup(v)

        return context
