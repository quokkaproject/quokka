# coding: utf-8

from flask import send_from_directory, current_app, request
from quokka.core.views import ContentDetail, ContentList
from quokka.core.models import Channel


def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)


def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


def configure(app):
    app.add_url_rule('/media/<path:filename>', view_func=media)

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
