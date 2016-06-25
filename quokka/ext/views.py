# coding: utf-8

import os
from flask import send_from_directory, current_app, request
from flask_security import roles_accepted
from quokka.core.views import (
    ContentDetail,
    ContentDetailPreview,
    ContentList,
    TagList
)
from quokka.core.views import TagAtom, FeedAtom, TagRss, FeedRss, SiteMap
from quokka.core.models.channel import Channel


@roles_accepted('admin', 'developer')
def template_files(filename):
    template_path = os.path.join(current_app.root_path,
                                 current_app.template_folder)
    return send_from_directory(template_path, filename)


@roles_accepted('admin', 'developer')
def theme_template_files(identifier, filename):
    template_path = os.path.join(
        current_app.root_path,
        "themes",
        identifier,
        "templates"
    )
    return send_from_directory(template_path, filename)


def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)


def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


def configure(app):
    app.add_quokka_url_rule('/sitemap.xml',
                            view_func=SiteMap.as_view('sitemap'))
    app.add_quokka_url_rule('/mediafiles/<path:filename>', view_func=media)
    app.add_quokka_url_rule('/template_files/<path:filename>',
                            view_func=template_files)
    app.add_quokka_url_rule(
        '/theme_template_files/<identifier>/<path:filename>',
        view_func=theme_template_files
    )
    for filepath in app.config.get('MAP_STATIC_ROOT', []):
        app.add_quokka_url_rule(filepath, view_func=static_from_root)

    # Match content detail, .html added to distinguish from channels
    # better way? how?
    content_extension = app.config.get("CONTENT_EXTENSION", "html")
    app.add_quokka_url_rule('/<path:long_slug>.{0}'.format(content_extension),
                            view_func=ContentDetail.as_view('detail'))

    # Draft preview
    app.add_quokka_url_rule('/<path:long_slug>.preview',
                            view_func=ContentDetailPreview.as_view('preview'))

    # Atom Feed
    app.add_quokka_url_rule(
        '/<path:long_slug>.atom',
        view_func=FeedAtom.as_view('atom_list')
    )
    app.add_quokka_url_rule(
        '/tag/<tag>.atom', view_func=TagAtom.as_view('atom_tag')
    )

    # RSS Feed
    app.add_quokka_url_rule(
        '/<path:long_slug>.xml', view_func=FeedRss.as_view('rss_list')
    )
    app.add_quokka_url_rule('/tag/<tag>.xml',
                            view_func=TagRss.as_view('rss_tag'))

    # Tag list
    app.add_quokka_url_rule('/tag/<tag>/', view_func=TagList.as_view('tag'))

    # Match channels by its long_slug mpath
    app.add_quokka_url_rule('/<path:long_slug>/',
                            view_func=ContentList.as_view('list'))
    # Home page
    app.add_quokka_url_rule(
        '/',
        view_func=ContentList.as_view('home'),
        defaults={"long_slug": Channel.get_homepage('long_slug') or "home"}
    )
