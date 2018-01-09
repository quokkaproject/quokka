# coding: utf-8

import os
from pathlib import Path
from flask import current_app, redirect, request, send_from_directory, url_for
from .sitemap import SiteMapView


def template_files(filename):
    template_path = os.path.join(current_app.root_path,
                                 current_app.template_folder)
    return send_from_directory(template_path, filename)


def theme_template_files(identifier, filename):
    template_path = os.path.join(
        current_app.root_path,
        "themes",
        identifier,
        "templates"
    )
    return send_from_directory(template_path, filename)


def media(filename):
    media_root = Path.cwd() / Path(current_app.config.get('MEDIA_ROOT'))
    return send_from_directory(media_root, filename)


def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


def configure(app):

    @app.route('/<prot>://<path:destiny>')
    def redir_to_external(prot, destiny):
        return redirect(f"{prot}://{destiny}")

    @app.route('/favicon.ico')
    def favicon():
        # TODO: Dynamize
        return redirect(url_for('static', filename='favicon.ico'), code=301)

    app.add_quokka_url_rule('/sitemap.xml',
                            view_func=SiteMapView.as_view('sitemap'))

    app.add_quokka_url_rule('/mediafiles/<path:filename>', view_func=media)

    app.add_quokka_url_rule('/template_files/<path:filename>',
                            view_func=template_files)

    app.add_quokka_url_rule(
        '/theme_template_files/<identifier>/<path:filename>',
        view_func=theme_template_files
    )

    for filepath in app.config.get('MAP_STATIC_ROOT', []):
        app.add_quokka_url_rule(filepath, view_func=static_from_root)
