from flask import redirect
from quokka.core.app import QuokkaModule
from .admin import ContentView
from .views import DetailView, PreviewView, ArticleListView, CategoryListView
# from .models import Content
from .utils import url_for_content, strftime


def configure(app):
    # Register admin views
    app.admin.register(
        app.db.index,
        ContentView,
        name='Content',
        endpoint='contentview'
    )

    # Admin admin index panel icons
    app.admin.add_icon(
        endpoint='quokka.core.content.admin.contentview.create_view',
        icon='glyphicon-file',
        text='New<br>Content'
    )

    app.admin.add_icon(
        endpoint='quokka.core.content.admin.contentview.index_view',
        icon='glyphicon-list',
        text='All<br>Content'
    )

    # Register new commands

    # Register content types

    # Register content formats

    # create new Quokka Module with its views
    module = QuokkaModule(__name__)
    ext = app.config.get("CONTENT_EXTENSION", "html")

    # handle /
    module.add_url_rule(
        '/',
        view_func=lambda: redirect(f'/index.{ext}'),
        endpoint='indexroot'
    )

    # handle /index.html
    module.add_url_rule(f'/index.{ext}',
                        view_func=ArticleListView.as_view('index'))

    # handle /2.html
    module.add_url_rule(f'/<int:page_number>.{ext}',
                        view_func=ArticleListView.as_view('index_numbered'))

    # handle /index2.html
    module.add_url_rule(f'/index<int:page_number>.{ext}',
                        view_func=ArticleListView.as_view('index_paginate'))

    # handle /article-name.html and /foo/bar/article-name.html
    module.add_url_rule(f'/<path:slug>.{ext}',
                        view_func=DetailView.as_view('detail'))

    # handle the .preview of drafts
    module.add_url_rule('/<path:slug>.preview',
                        view_func=PreviewView.as_view('preview'))

    # handle /category/
    module.add_url_rule(
        f'/category/',
        view_func=lambda: redirect(f'/category/index.{ext}'),
        endpoint='categoryroot'
    )

    # handle /category/index.html
    module.add_url_rule(f'/category/index.{ext}',
                        view_func=CategoryListView.as_view('category_index'))

    # handle /category/foo.html and /category/foo/bar.html
    module.add_url_rule(f'/category/<path:category>.{ext}',
                        view_func=ArticleListView.as_view('category'))

    # handle /category/foo2.html and /category/foo/bar2.html
    module.add_url_rule(f'/category/<path:category><int:page_number>.{ext}',
                        view_func=ArticleListView.as_view('category_paginate'))

    # add template globals to app
    app.add_template_global(url_for_content)
    app.add_template_filter(strftime)

    # add context processors
    @module.context_processor
    def theme_context():
        return {
            'FOO': 'BAR'
        }

    # register the module
    app.register_module(module)
