import jinja2
from flask import send_from_directory
from pathlib import Path


def configure(app):
    THEME_FOLDER = Path(app.config.get('THEME_FOLDER', 'themes'))
    THEME_ACTIVE = Path(app.config.get('THEME_ACTIVE', 'Flex'))
    THEME_TEMPLATE_FOLDER = THEME_FOLDER / THEME_ACTIVE / Path('templates')
    THEME_STATIC_FOLDER = THEME_FOLDER / THEME_ACTIVE / Path('static')
    ABS_THEME_STATIC_FOLDER = Path.cwd() / THEME_STATIC_FOLDER

    my_loader = jinja2.ChoiceLoader([
        # TODO: add theme based overload for themes
        # example, replace `comments.html` for template
        QuokkaTemplateLoader([THEME_TEMPLATE_FOLDER]),
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
            '>Pelican', '>Quokka CMS'
        ).replace(
            '>pelican', '>Quokka CMS'
        )

        # TODO: Fix pelican unrendered footer

        return contents, filename, uptodate
