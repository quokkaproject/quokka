# coding: utf-8

import os
from flask import send_from_directory, current_app, request
from flask.ext.security import roles_accepted
from quokka.core.views import ContentDetail, ContentList
from quokka.core.models import Channel


@roles_accepted('admin', 'developer')
def template_files(filename):
    template_path = os.path.join(current_app.root_path,
                                 current_app.template_folder)
    return send_from_directory(template_path, filename)


def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)


def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


def configure(app):
    app.add_url_rule('/mediafiles/<path:filename>', view_func=media)
    app.add_url_rule('/template_files/<path:filename>',
                     view_func=template_files)

    for filepath in app.config.get('MAP_STATIC_ROOT', []):
        app.add_url_rule(filepath, view_func=static_from_root)

    # Match content detail, .html added to distinguish from channels
    # better way? how?
    app.add_url_rule('/<path:long_slug>.html',
                     view_func=ContentDetail.as_view('detail'))
    # Match channels by its long_slug mpath
    app.add_url_rule('/<path:long_slug>/',
                     view_func=ContentList.as_view('list'))
    # Home page
    app.add_url_rule(
        '/',
        view_func=ContentList.as_view('home'),
        defaults={"long_slug": Channel.get_homepage('slug') or "home"}
    )
