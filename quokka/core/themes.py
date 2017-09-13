# coding: utf-8

from __future__ import with_statement
from pathlib import Path
import jinja2
import itertools
import logging
import os
import os.path
import re
import sys
# Yarg, here be pirates!
from operator import attrgetter

from flask import (Blueprint, abort, json, render_template,  # Module,
                   send_from_directory, url_for)
from jinja2 import contextfunction
from jinja2.loaders import BaseLoader, FileSystemLoader, TemplateNotFound
from werkzeug import cached_property


# Support >= Flask 0.9
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


logger = logging.getLogger()

DOCTYPES = 'html4 html5 xhtml'.split()
IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

containable = lambda i: i if hasattr(i, '__contains__') else tuple(i)  # noqa
if sys.version_info.major == 3:
    basestring = str


def starchain(i):
    return itertools.chain(*i)


def active_theme(ctx):
    if '_theme' in ctx:
        return ctx['_theme']
    elif ctx.name.startswith('_themes/'):
        return ctx.name[8:].split('/', 1)[0]
    else:
        raise RuntimeError("Could not find the active theme")


@contextfunction
def global_theme_template(ctx, templatename, fallback=True):
    theme = active_theme(ctx)
    templatepath = '_themes/%s/%s' % (theme, templatename)
    if (not fallback) or template_exists(templatepath):
        return templatepath
    else:
        return templatename


@contextfunction
def global_theme_static(ctx, filename, external=False, *args, **kwargs):
    theme = active_theme(ctx)
    return static_file_url(theme, filename, external, *args, **kwargs)


@contextfunction
def global_theme_get_info(ctx, attribute_name, fallback=''):
    theme = get_theme(active_theme(ctx))
    try:
        info = getattr(theme, attribute_name)
        if info is None:
            raise AttributeError(
                "Got None for getattr(theme, '{0}')".format(attribute_name))
        return info
    except AttributeError:
        pass
    return theme.options.get(attribute_name, fallback)


def static_file_url(theme, filename, external=False, *args, **kwargs):
    """
    This is a shortcut for getting the URL of a static file in a theme.

    :param theme: A `Theme` instance or identifier.
    :param filename: The name of the file.
    :param external: Whether the link should be external or not. Defaults to
                     `False`.
    """
    if isinstance(theme, Theme):
        theme = theme.identifier
    return url_for('_themes.static', themeid=theme, filename=filename,
                   _external=external, *args, **kwargs)


def render_theme_template(theme, template_name, _fallback=True, **context):
    """
    This renders a template from the given theme. For example::

        return render_theme_template(g.user.theme, 'index.html', posts=posts)

    If `_fallback` is True and the template does not exist within the theme,
    it will fall back on trying to render the template using the application's
    normal templates. (The "active theme" will still be set, though, so you
    can try to extend or include other templates from the theme.)

    :param theme: Either the identifier of the theme to use, or an actual
                  `Theme` instance.
    :param template_name: The name of the template to render.
    :param _fallback: Whether to fall back to the default
    """

    if not isinstance(theme, (list, tuple)):
        theme = [theme]

    logger.debug("Rendering template")
    logger.debug("theme {} - template {} - fallback {} - context {}".format(
        theme, template_name, _fallback, context))

    if not isinstance(template_name, (list, tuple)):
        template_name = [template_name]

    last = template_name.pop()

    themes = theme

    for name in template_name:
        for theme in themes:
            if isinstance(theme, Theme):
                theme = theme.identifier
            context['_theme'] = theme

            try:
                logger.debug(
                    "trying to render {} in {}".format(name, theme)
                )
                return render_template('_themes/%s/%s' % (theme, name),
                                       **context)
            except TemplateNotFound:
                logger.debug(
                    "{} not found in {}, trying next...".format(name, theme))
                continue

    if _fallback:
        logger.debug("Fallback to app templates folder")
        for name in template_name:
            try:
                logger.debug(
                    "trying to render {} in app templates".format(name))
                return render_template(name, **context)
            except TemplateNotFound:
                logger.debug("{} not found, trying next...".format(name))
                continue

    for theme in themes:
        if isinstance(theme, Theme):
            theme = theme.identifier
        context['_theme'] = theme

        try:
            logger.debug(
                "Trying to load last template {} in {}".format(last, theme))
            return render_template('_themes/%s/%s' % (theme, last), **context)
        except TemplateNotFound:
            continue

    if _fallback:
        logger.debug(
            "Trying to load last template {} in app templates".format(last))
        return render_template(last, **context)

    logger.debug("Template {} not found".format(last))

    raise

# convenience


def get_theme(ident):
    """
    This gets the theme with the given identifier from the current app's
    theme manager.

    :param ident: The theme identifier.
    """
    ctx = stack.top
    return ctx.app.theme_manager.themes[ident]


def get_themes_list():
    """
    This returns a list of all the themes in the current app's theme manager,
    sorted by identifier.
    """
    ctx = stack.top
    return list(ctx.app.theme_manager.list_themes())


def static(themeid, filename):
    try:
        ctx = stack.top
        theme = ctx.app.theme_manager.themes[themeid]
    except KeyError:
        abort(404)
    return send_from_directory(theme.static_path, filename)


def template_exists(templatename):
    ctx = stack.top
    return templatename in containable(ctx.app.jinja_env.list_templates())

# loaders


def list_folders(path):
    """
    This is a helper function that only returns the directories in a given
    folder.

    :param path: The path to list directories in.
    """
    return (name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)))


def load_themes_from(path):
    """
    This is used by the default loaders. You give it a path, and it will find
    valid themes and yield them one by one.

    :param path: The path to search for themes in.
    """
    for basename in (b for b in list_folders(path) if IDENTIFIER.match(b)):
        try:
            t = Theme(os.path.join(path, basename))
        except:
            pass
        else:
            if t.identifier == basename:
                yield t


def packaged_themes_loader(app):
    """
    This theme will find themes that are shipped with the application. It will
    look in the application's root path for a ``themes`` directory - for
    example, the ``someapp`` package can ship themes in the directory
    ``someapp/themes/``.
    """
    themes_path = os.path.join(app.root_path, 'themes')
    if os.path.exists(themes_path):
        return load_themes_from(themes_path)
    else:
        return ()


def theme_paths_loader(app):
    """
    This checks the app's `THEME_PATHS` configuration variable to find
    directories that contain themes. The theme's identifier must match the
    name of its directory.
    """
    theme_paths = app.config.get('THEME_PATHS', ())
    if isinstance(theme_paths, basestring):
        theme_paths = [p.strip() for p in theme_paths.split(';')]
    return starchain(
        load_themes_from(path) for path in theme_paths
    )


class ThemeTemplateLoader(BaseLoader):
    """
    This is a template loader that loads templates from the current app's
    loaded themes.
    """
    def __init__(self, as_blueprint=False):
        self.as_blueprint = as_blueprint
        BaseLoader.__init__(self)

    def get_source(self, environment, template):
        if self.as_blueprint and template.startswith("_themes/"):
            template = template[8:]
        try:
            themename, templatename = template.split('/', 1)
            ctx = stack.top
            theme = ctx.app.theme_manager.themes[themename]
        except (ValueError, KeyError):
            raise TemplateNotFound(template)
        try:
            return theme.jinja_loader.get_source(environment, templatename)
        except TemplateNotFound:
            raise TemplateNotFound(template)

    def list_templates(self):
        res = []
        ctx = stack.top
        fmt = '_themes/{}/{}'
        for ident, theme in ctx.app.theme_manager.themes.items():
            if sys.version_info.major == 2:
                res.extend(
                    (fmt.format(str(ident), str(t))).encode("utf-8")
                    for t in theme.jinja_loader.list_templates()
                )
            elif sys.version_info.major == 3:
                res.extend(fmt.format(str(ident), str(t)) for t in
                           theme.jinja_loader.list_templates())
        return res


#########################################################################

themes_blueprint = Blueprint('_themes', __name__, url_prefix='/_themes')
themes_blueprint.jinja_loader = ThemeTemplateLoader(True)
themes_blueprint.add_url_rule(
    '/<themeid>/<path:filename>', 'static',
    view_func=static
)


class Themes(object):
    """ This is the main class you will use to interact
        with Flask-Themes2 on your app.

        It really only implements the bare minimum, the rest
        is passed through to other methods and classes.
    """

    def __init__(self, app=None, **kwargs):
        """ If given an app, this will simply call
            init_themes, and pass through all kwargs
            to init_themes, making it super easy.

            :param app: the `~flask.Flask` instance to setup themes for.
            :param \*\*kwargs: keyword args to pass through to init_themes
        """
        if app is not None:
            self._app = app
            self.init_themes(self._app, **kwargs)
        else:
            self._app = None

    def init_themes(self, app, loaders=None, app_identifier=None,
                    manager_cls=None, theme_url_prefix="/_themes"):
        """ This sets up the theme infrastructure by adding a `ThemeManager`
            to the
            given app and registering the module/blueprint containing the
            views and templates needed.

            :param app: The `~flask.Flask` instance to set up themes for.
            :param loaders: An iterable of loaders to use.
              It defaults to `packaged_themes_loader` and `theme_paths_loader`.
            :param app_identifier: The application identifier to use.
              If not given, it defaults to the app's import name.
            :param manager_cls: If you need a custom manager class,
               you can pass it in here.
            :param theme_url_prefix: The prefix to use for the URLs on
               the themes module. (Defaults to ``/_themes``.)
        """
        if app_identifier is None:
            app_identifier = app.import_name
        if manager_cls is None:
            manager_cls = ThemeManager
        manager_cls(app, app_identifier, loaders=loaders)

        app.jinja_env.globals['theme'] = global_theme_template
        app.jinja_env.globals['theme_static'] = global_theme_static
        app.jinja_env.globals['theme_get_info'] = global_theme_get_info
        app.register_blueprint(themes_blueprint, url_prefix=theme_url_prefix)


class ThemeManager(object):
    """
    This is responsible for loading and storing all the themes for an
    application. Calling `refresh` will cause it to invoke all of the theme
    loaders.

    A theme loader is simply a callable that takes an app and returns an
    iterable of `Theme` instances. You can implement your own loaders if your
    app has another way to load themes.

    :param app: The app to bind to. (Each instance is only usable for one
                app.)
    :param app_identifier: The value that the info.json's `application` key
                           is required to have. If you require a more complex
                           check, you can subclass and override the
                           `valid_app_id` method.
    :param loaders: An iterable of loaders to use. The defaults are
                    `packaged_themes_loader` and `theme_paths_loader`, in that
                    order.
    """
    def __init__(self, app, app_identifier, loaders=None):
        self.bind_app(app)
        self.app_identifier = app_identifier

        self._themes = None

        #: This is a list of the loaders that will be used to load the themes.
        self.loaders = []
        if loaders:
            self.loaders.extend(loaders)
        else:
            self.loaders.extend((packaged_themes_loader, theme_paths_loader))

    @property
    def themes(self):
        """
        This is a dictionary of all the themes that have been loaded. The keys
        are the identifiers and the values are `Theme` objects.
        """
        if self._themes is None:
            self.refresh()
        return self._themes

    def list_themes(self):
        """
        This yields all the `Theme` objects, in sorted order.
        """
        return sorted(self.themes.values(), key=attrgetter('identifier'))

    def bind_app(self, app):
        """
        If an app wasn't bound when the manager was created, this will bind
        it. The app must be bound for the loaders to work.

        :param app: A `~flask.Flask` instance.
        """
        self.app = app
        app.theme_manager = self

    def valid_app_id(self, app_identifier):
        """
        This checks whether the application identifier given will work with
        this application. The default implementation checks whether the given
        identifier matches the one given at initialization.

        :param app_identifier: The application identifier to check.
        """
        return self.app_identifier == app_identifier

    def refresh(self):
        """
        This loads all of the themes into the `themes` dictionary. The loaders
        are invoked in the order they are given, so later themes will override
        earlier ones. Any invalid themes found (for example, if the
        application identifier is incorrect) will be skipped.
        """
        self._themes = {}
        for theme in starchain(ldr(self.app) for ldr in self.loaders):
            if self.valid_app_id(theme.application):
                self.themes[theme.identifier] = theme


class Theme(object):
    """
    This contains a theme's metadata.

    :param path: The path to the theme directory.
    """
    def __init__(self, path):
        #: The theme's root path. All the files in the theme are under this
        #: path.
        self.path = os.path.abspath(path)

        with open(os.path.join(self.path, 'info.json')) as fd:
            self.info = i = json.load(fd)

        #: The theme's name, as given in info.json. This is the human
        #: readable name.
        self.name = i['name']

        #: The application identifier given in the theme's info.json. Your
        #: application will probably want to validate it.
        self.application = i['application']

        #: The theme's identifier. This is an actual Python identifier,
        #: and in most situations should match the name of the directory the
        #: theme is in.
        try:
            self.identifier = path.split('/')[-1]
        except:
            self.identifier = i.get('identifier')

        #: The human readable description. This is the default (English)
        #: version.
        self.description = i.get('description')

        #: This is a dictionary of localized versions of the description.
        #: The language codes are all lowercase, and the ``en`` key is
        #: preloaded with the base description.
        self.localized_desc = dict(
            (k.split('_', 1)[1].lower(), v) for k, v in i.items()
            if k.startswith('description_')
        )
        self.localized_desc.setdefault('en', self.description)

        #: The author's name, as given in info.json. This may or may not
        #: include their email, so it's best just to display it as-is.
        self.author = i['author']

        #: A short phrase describing the license, like "GPL", "BSD", "Public
        #: Domain", or "Creative Commons BY-SA 3.0".
        self.license = i.get('license')

        #: A URL pointing to the license text online.
        self.license_url = i.get('license_url')

        #: The URL to the theme's or author's Web site.
        self.website = i.get('website')

        #: The theme's preview image, within the static folder.
        self.preview = i.get('preview')

        #: The theme's doctype. This can be ``html4``, ``html5``, or ``xhtml``
        #: with html5 being the default if not specified.
        self.doctype = i.get('doctype', 'html5')

        #: The theme's version string.
        self.version = i.get('version')

        #: Any additional options. These are entirely application-specific,
        #: and may determine other aspects of the application's behavior.
        self.options = i.get('options', {})

    @cached_property
    def static_path(self):
        """
        The absolute path to the theme's static files directory.
        """
        return os.path.join(self.path, 'static')

    @cached_property
    def templates_path(self):
        """
        The absolute path to the theme's templates directory.
        """
        return os.path.join(self.path, 'templates')

    @cached_property
    def license_text(self):
        """
        The contents of the theme's license.txt file, if it exists. This is
        used to display the full license text if necessary. (It is `None` if
        there was not a license.txt.)
        """
        lt_path = os.path.join(self.path, 'license.txt')
        if os.path.exists(lt_path):
            with open(lt_path) as fd:
                return fd.read()
        else:
            return None

    @cached_property
    def jinja_loader(self):
        """
        This is a Jinja2 template loader that loads templates from the theme's
        ``templates`` directory.
        """
        return FileSystemLoader(self.templates_path)


def configure(app):
    # themes = Themes()
    # themes.init_themes(app, app_identifier="quokka")
    # app.jinja_loader = ThemeTemplateLoader()

    THEME_FOLDER = Path(app.config.get('THEME_FOLDER', 'themes'))
    THEME_ACTIVE = Path(app.config.get('THEME_ACTIVE', 'Flex'))
    THEME_TEMPLATE_FOLDER = THEME_FOLDER / THEME_ACTIVE / Path('templates')
    THEME_STATIC_FOLDER = THEME_FOLDER / THEME_ACTIVE / Path('static')
    ABS_THEME_STATIC_FOLDER = Path.cwd() / THEME_STATIC_FOLDER

    my_loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader([THEME_TEMPLATE_FOLDER]),
        app.jinja_loader
    ])
    app.jinja_loader = my_loader

    @app.route('/theme/<path:filename>')
    def theme_static(filename):
        return send_from_directory(ABS_THEME_STATIC_FOLDER, filename)
