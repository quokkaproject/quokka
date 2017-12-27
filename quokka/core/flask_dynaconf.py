# coding: utf-8
"""This core extension cannot be loaded from settings.yml
should be loaded directly in create_app"""

from flask import Markup
from dynaconf.contrib import FlaskDynaconf
from dynaconf.loaders import yaml_loader, env_loader


def configure_dynaconf(app):
    # extra vars in .secrets.yml override values on quokka.yml
    # secrets file is a hidden file and must be excluded on .gitignore
    # all password, token and other sensitive must go there
    # or exported as env var ex: QUOKKA_SECRET_KEY=12345

    settings_file = 'quokka.yml,.secrets.yml'
    initial_envmode = app.config.get('ENVMODE')

    # Extension is supposed to override envmode
    FlaskDynaconf(
        app,
        ENVVAR_FOR_DYNACONF="QUOKKA_SETTINGS_MODULE",
        DYNACONF_NAMESPACE='QUOKKA',
        SETTINGS_MODULE_FOR_DYNACONF=settings_file,
        DYNACONF_SILENT_ERRORS=True
    )

    # Configure extra environment
    envmode = initial_envmode or app.config.get('ENVMODE')
    if envmode is not None:
        yaml_loader.load(
            obj=app.config,
            namespace=envmode,
            filename=settings_file
        )
        # overload with envvars
        env_loader.load_from_env(
            identifier=envmode,
            key=None,
            namespace=f'quokka_{envmode}',
            obj=app.config,
            silent=True
        )

    # configure theme options
    app.theme_context = {
        'JINJA_ENVIRONMENT': app.jinja_env,
        'DEFAULT_LANG': app.config.get('BABEL_DEFAULT_LOCALE'),
        'default_locale': app.config.get('BABEL_DEFAULT_LOCALE'),
        'PAGES': [],
        'pages': [],
        'tags': [],
        'articles': [],
        'categories': [],
        # https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud
        'tag_cloud': [],
        'CATEGORIES_URL': 'categories/index.html',
        'JINJA_EXTENSIONS': app.jinja_env.extensions,
        'USE_LESS': False,
        # For some themes like bootstrap3 theme SITEURL must be ''
        'SITEURL': 'http://localhost:5000',
        'THEME_STATIC_DIR': 'theme',
        'FAVICON': 'favicon.ico',
        'FAVICON_IE': 'favicon.ico',
        'FAVICON_FILENAME': 'favicon.ico',
        # 'AVATAR': 'LOAD FROM UPLOADS',
        'NEWEST_FIRST_ARCHIVES': True
    }
    # load theme variables from YAML file
    yaml_loader.load(
        obj=app.theme_context,
        namespace='theme',
        filename=app.config.get('SETTINGS_MODULE')
    )
    # overrride with QUOKKA_THEME_ prefixed env vars if exist
    env_loader.load_from_env(
        identifier='theme',
        key=None,
        namespace='quokka_theme',
        obj=app.theme_context,
        silent=True
    )

    # remove prefix for pelican-themes
    active = app.theme_context.get('ACTIVE', 'default')
    if active.startswith('pelican'):
        active = active.lstrip('pelican-')
    app.theme_context['ACTIVE'] = active

    # load theme specific variables from YAML
    yaml_loader.load(
        obj=app.theme_context,
        namespace=f'theme_{app.theme_context.get("ACTIVE")}',
        filename=app.config.get('SETTINGS_MODULE')
    )
    # overrride with QUOKKA_THEME_THEMENAME prefixed env vars if exist
    env_loader.load_from_env(
        identifier=f'theme_{app.theme_context.get("ACTIVE")}',
        key=None,
        namespace=f'quokka_theme_{app.theme_context.get("ACTIVE")}',
        obj=app.theme_context,
        silent=True
    )

    # mark strings as safe Markup
    for k, v in app.theme_context.items():
        if isinstance(v, str):
            app.theme_context[k] = Markup(v)
