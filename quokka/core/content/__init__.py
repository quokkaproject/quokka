from quokka.core.app import QuokkaModule
from .admin import AdminArticlesView, AdminPagesView
from .views import (
    DetailView, PreviewView, ArticleListView, CategoryListView, TagListView,
    AuthorListView
)
from .utils import url_for_content, strftime


def configure(app):
    # Register admin views
    app.admin.register(
        app.db.index,
        AdminArticlesView,
        name='Articles',
        endpoint='articleview'
    )

    app.admin.register(
        app.db.index,
        AdminPagesView,
        name='Pages',
        endpoint='pageview'
    )

    # Admin admin index panel icons
    app.admin.add_icon(
        endpoint='quokka.core.content.admin.articleview.create_view',
        icon='glyphicon-list-alt',
        text='New<br>Article'
    )

    app.admin.add_icon(
        endpoint='quokka.core.content.admin.pageview.create_view',
        icon='glyphicon-file',
        text='New<br>Page'
    )

    # app.admin.add_icon(
    #     endpoint='quokka.core.content.admin.articleview.index_view',
    #     icon='glyphicon-list',
    #     text='All<br>Articles'
    # )

    # Register new commands

    # Register content types

    # Register content formats

    # create new Quokka Module with its views
    module = QuokkaModule(__name__)
    ext = app.config.get("CONTENT_EXTENSION", "html")

    # INDEX|HOME
    # handle /
    module.add_url_rule('/', view_func=ArticleListView.as_view('index'))
    # handle /index.html
    module.add_url_rule(f'/index.{ext}',
                        view_func=ArticleListView.as_view('indexnamed'))
    # handle /2/
    module.add_url_rule(f'/<int:page_number>/',
                        view_func=ArticleListView.as_view('indexpag'))
    # handle /2.html
    module.add_url_rule(f'/<int:page_number>.{ext}',
                        view_func=ArticleListView.as_view('indexpagext'))
    # handle /2/index.html
    module.add_url_rule(f'/<int:page_number>/index.{ext}',
                        view_func=ArticleListView.as_view('indexpagnamed'))

    # USER
    # handle /@authorname/
    # handle /@authorname/2/
    # handle /@authorname/index.html
    # handle /@authorname/2.html
    # handle /@authorname/2/index.html

    # AUTHORS
    # handle /authors/
    module.add_url_rule(f'/authors/',
                        view_func=AuthorListView.as_view('authors'))
    # handle /authors/index.html
    module.add_url_rule(f'/authors/index.{ext}',
                        view_func=AuthorListView.as_view('authorsnamed'))
    # AUTHOR
    # handle /author/name/
    module.add_url_rule('/author/<path:author>/',
                        view_func=ArticleListView.as_view('author'))

    # handle /author/name/index.html
    module.add_url_rule(f'/author/<path:author>/index.{ext}',
                        view_func=ArticleListView.as_view('authornamed'))

    # handle /author/name/2
    module.add_url_rule('/author/<path:author>/<int:page_number>/',
                        view_func=ArticleListView.as_view('authorpag'))

    # handle /author/name/2.html
    module.add_url_rule(f'/author/<path:author>/<int:page_number>.{ext}',
                        view_func=ArticleListView.as_view('authorpagext'))

    # handle /author/name/2/index.html
    module.add_url_rule(f'/author/<path:author>/<int:page_number>/index.{ext}',
                        view_func=ArticleListView.as_view('authorpagnamed'))

    # TAGS
    # handle /tags/
    module.add_url_rule(f'/tags/',
                        view_func=TagListView.as_view('tags'))
    # handle /tags/index.html
    module.add_url_rule(f'/tags/index.{ext}',
                        view_func=TagListView.as_view('tagsnamed'))
    # TAG
    # handle /tag/tagname/
    module.add_url_rule('/tag/<string:tag>/',
                        view_func=ArticleListView.as_view('tag'))
    # handle /tag/tagname/index.html
    module.add_url_rule(f'/tag/<string:tag>/index.{ext}',
                        view_func=ArticleListView.as_view('tagnamed'))
    # handle /tag/tagname/2/
    module.add_url_rule('/tag/<string:tag>/<int:page_number>/',
                        view_func=ArticleListView.as_view('tagpag'))
    # handle /tag/tagname/2.html
    module.add_url_rule(f'/tag/<string:tag>/<int:page_number>.{ext}',
                        view_func=ArticleListView.as_view('tagpagext'))
    # handle /tag/tagname/2/index.html
    module.add_url_rule(f'/tag/<string:tag>/<int:page_number>/index.{ext}',
                        view_func=ArticleListView.as_view('tagpagnamed'))

    # CATEGORIES
    # handle /categories/
    module.add_url_rule(f'/categories/',
                        view_func=CategoryListView.as_view('categories'))
    # handle /categories/index.html
    module.add_url_rule(f'/categories/index.{ext}',
                        view_func=CategoryListView.as_view('categoriesnamed'))
    # CATEGORY
    # handle /blog/subcategory/
    module.add_url_rule('/<path:category>/',
                        view_func=ArticleListView.as_view('cat'))
    # handle /blog/subcategory/index.html
    module.add_url_rule(f'/<path:category>/index.{ext}',
                        view_func=ArticleListView.as_view('catnamed'))
    # handle /blog/subcategory/2/
    module.add_url_rule(f'/<path:category>/<int:page_number>/',
                        view_func=ArticleListView.as_view('catpag'))
    # handle /blog/subcategory/2.html
    module.add_url_rule(f'/<path:category>/<int:page_number>.{ext}',
                        view_func=ArticleListView.as_view('catpagext'))
    # handle /blog/subcategory/2/index.html
    module.add_url_rule(f'/<path:category>/<int:page_number>/index.{ext}',
                        view_func=ArticleListView.as_view('catpagnamed'))

    # ARTICLE|PAGE
    # handle /article-name.html and /foo/bar/article-name.html
    module.add_url_rule(f'/<path:slug>.{ext}',
                        view_func=DetailView.as_view('detail'))

    # handle the .preview of drafts
    module.add_url_rule('/<path:slug>.preview',
                        view_func=PreviewView.as_view('preview'))

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
