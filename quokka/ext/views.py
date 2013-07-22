# coding: utf-8

from quokka.core.views import ContentDetail, ContentList
from quokka.core.models import Channel


def configure(app):
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
