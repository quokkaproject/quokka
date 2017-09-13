# coding: utf-8

# import datetime
from flask import Markup
from dynaconf.loaders import yaml_loader


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
            'SITEURL': 'http://localhost:5000',
            'THEME_STATIC_DIR': 'theme',
            'FAVICON': 'favicon.ico',
            'AVATAR': 'LOAD FROM UPLOADS'
        }

        yaml_loader.load(
            obj=context,
            namespace='pelican',
            filename=app.config.get('SETTINGS_MODULE')
        )

        yaml_loader.load(
            obj=context,
            namespace=f'pelican_{app.config.get("THEME_ACTIVE")}',
            filename=app.config.get('SETTINGS_MODULE')
        )

        if 'SHARIFF_SERVICES' in context:
            context['SHARIFF_SERVICES'] = Markup(context['SHARIFF_SERVICES'])

        # TODO: LOAD PELICAN CONF FROM MODEL
        # with app.config.using_namespace('pelican'):

        #     pelican = {
        #         # pelican defaults
        #         'PYGMENTS_STYLE': app.config.get('PYGMENTS_STYLE', 'github'),
        #         'CUSTOM_CSS': app.config.get('CUSTOM_CSS'),
        #         'DOCUTIL_CSS': app.config.get('DOCUTIL_CSS'),
        #         'TYPOGRIFY': app.config.get('TYPOGRIFY'),
        #         'FEED_ALL_ATOM': app.config.get('FEED_ALL_ATOM'),
        #         'FEED_ALL_RSS': app.config.get('FEED_ALL_RSS'),
        #         'FEED_DOMAIN': app.config.get('FEED_DOMAIN'),
        #         'FAVICON': app.config.get('FAVICON'),
        #         'BROWSER_COLOR': app.config.get('BROWSER_COLOR'),
        #         'AUTHOR': app.config.get('AUTHOR'),
        #         'SITEDESCRIPTION': app.config.get('SITEDESCRIPTION'),
        #         'SITENAME': app.config.get('SITENAME'),
        #         'HIDE_SITENAME': app.config.get('HIDE_SITENAME'),
        #         'SITETITLE': app.config.get('SITETITLE'),
        #         'SITESUBTITLE': app.config.get('SITESUBTITLE'),
        #         'GOOGLE_ADSENSE': app.config.get('GOOGLE_ADSENSE'),
        #         'GOOGLE_TAG_MANAGER': app.config.get('GOOGLE_TAG_MANAGER'),
        #         'SITELOGO': app.config.get('SITELOGO'),
        #         'LINKS': app.config.get('LINKS'),
        #         'PAGES_SORT_ATTRIBUTE': app.config.get('PAGES_SORT_ATTRIBUTE'),
        #         'SOCIAL': app.config.get('SOCIAL'),
        #         'MAIN_MENU': app.config.get('MAIN_MENU'),
        #         'MENUITEMS': app.config.get('MENUITEMS'),
        #         'CC_LICENSE': app.config.get('CC_LICENSE'),
        #         'GOOGLE_ANALYTICS': app.config.get('GOOGLE_ANALYTICS'),
        #         'GUAGES': app.config.get('GUAGES'),
        #         'ADD_THIS_ID': app.config.get('ADD_THIS_ID'),
        #         'PIWIK_URL': app.config.get('PIWIK_URL'),
        #         'GITHUB_CORNER_URL': app.config.get('GITHUB_CORNER_URL'),
        #         'USE_OPEN_GRAPH': app.config.get('USE_OPEN_GRAPH'),
        #         'OPEN_GRAPH_FB_APP_ID': app.config.get('OPEN_GRAPH_FB_APP_ID'),
        #         'OPEN_GRAPH_IMAGE': app.config.get('OPEN_GRAPH_IMAGE'),
        #         'PLUGINS': app.config.get('PLUGINS'),
        #         'FAVICON_IE': app.config.get('FAVICON_IE'),
        #         'TOUCHICON': app.config.get('TOUCHICON'),
        #         'BOOTSTRAP_THEME': app.config.get('BOOTSTRAP_THEME'),
        #         'BOOTSTRAP_NAVBAR_INVERSE': app.config.get('BOOTSTRAP_NAVBAR_INVERSE'),
        #         'DISPLAY_PAGES_ON_MENU': app.config.get('DISPLAY_PAGES_ON_MENU'),
        #         'DISPLAY_CATEGORIES_ON_MENU': app.config.get('DISPLAY_CATEGORIES_ON_MENU'),
        #         'ARCHIVES_URL': app.config.get('ARCHIVES_URL'),
        #         'BANNER': app.config.get('BANNER'),
        #         'BANNER_ALL_PAGES': app.config.get('BANNER_ALL_PAGES'),
        #         'HIDE_SIDEBAR': app.config.get('HIDE_SIDEBAR'),
        #         'ABOUT_ME': app.config.get('ABOUT_ME'),
        #     }
        return context
