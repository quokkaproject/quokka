from flask import url_for
from quokka.core.app import QuokkaModule
from .admin import ContentView
from .views import DetailView, PreviewView, ArticleListView
from .models import Content
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
    content_extension = app.config.get("CONTENT_EXTENSION", "html")
    module.add_url_rule('/<path:slug>.{0}'.format(content_extension),
                        view_func=DetailView.as_view('detail'))

    module.add_url_rule('/<path:slug>.preview',
                        view_func=PreviewView.as_view('preview'))

    module.add_url_rule('/<path:category>/',
                        view_func=ArticleListView.as_view('category'))

    module.add_url_rule('/',
                        view_func=ArticleListView.as_view('index'))

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
