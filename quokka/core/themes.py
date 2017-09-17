import jinja2
from flask import send_from_directory
from pathlib import Path


def configure(app):
    OVERLOAD_ENABLED = app.theme_context.get('OVERLOAD_ENABLED', True)
    TEMPLATES = Path('templates')
    THEME_FOLDER = Path(app.theme_context.get('FOLDER', 'themes'))
    THEME_ACTIVE = Path(app.theme_context.get('ACTIVE', 'bootstrap3'))
    THEME_TEMPLATE_FOLDER = THEME_FOLDER / THEME_ACTIVE / TEMPLATES
    THEME_STATIC_FOLDER = THEME_FOLDER / THEME_ACTIVE / Path('static')
    ABS_THEME_STATIC_FOLDER = Path.cwd() / THEME_STATIC_FOLDER
    DEFAULT_PATH = Path(app.jinja_loader.searchpath[0])
    OVERLOAD_FOLDER = DEFAULT_PATH / f'overload_{THEME_ACTIVE}' / TEMPLATES

    FOLDERS = [THEME_TEMPLATE_FOLDER]
    if OVERLOAD_ENABLED:
        FOLDERS.insert(0, OVERLOAD_FOLDER)

    my_loader = jinja2.ChoiceLoader([
        # TODO: add theme based overload for themes
        # example, replace `comments.html` for template
        QuokkaTemplateLoader(FOLDERS),
        app.jinja_loader
    ])
    app.jinja_loader = my_loader

    @app.route('/theme/<path:filename>')
    def theme_static(filename):
        return send_from_directory(ABS_THEME_STATIC_FOLDER, filename)


class QuokkaTemplateLoader(jinja2.FileSystemLoader):
    def get_source(self, environment, template):
        contents, filename, uptodate = super().get_source(environment,
                                                          template)

        # re-branding
        contents = contents.replace(
            'blog.getpelican.com', 'quokkaproject.org'
        ).replace(
            'docs.getpelican.com', 'quokkaproject.org'
        ).replace(
            'getpelican.com', 'quokkaproject.org'
        ).replace(
            '>pelican-', '>theme-'
        ).replace(
            '>Pelican', '>Quokka CMS'
        ).replace(
            '>pelican', '>Quokka CMS'
        )

        # TODO: Fix pelican unrendered footer

        return contents, filename, uptodate
