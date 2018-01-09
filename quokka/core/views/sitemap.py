from flask import render_template
from flask import current_app as app
from flask.views import MethodView
from quokka.core.content.models import make_model


class SiteMapView(MethodView):

    def get_contents(self):
        """
        TODO: Should include extra paths, fixed paths
        config based paths, static paths
        """
        return (
            self.get_index() +
            self.get_categories() +
            self.get_tags() +
            self.get_authors() +
            self.get_articles_and_pages()
        )

    def get_index(self):
        return [
            make_model(app.theme_context.get('INDEX_CATEGORY'),
                       content_type='category')
        ] + [
            make_model(item, content_type='category')
            for item in app.theme_context.get('LIST_CATEGORIES', [])
        ]

    def get_articles_and_pages(self):
        return [
            make_model(item)
            for item in app.db.content_set(
                {'published': True,
                 'content_type': {'$in': ['article', 'page']}},
                sort=app.theme_context.get('ARTICLE_ORDER_BY', [('date', -1)])
            )
        ]

    def get_categories(self):
        return [
            make_model('categories', content_type='fixed')
        ] + [
            make_model(item, content_type='category')
            for item in app.db.category_set()
        ]

    def get_tags(self):
        return [
            make_model('tags', content_type='fixed')
        ] + [
            make_model(item, content_type='tag')
            for item in app.db.tag_set()
        ]

    def get_authors(self):
        return [
            make_model('authors', content_type='fixed')
        ] + [
            make_model(item, content_type='author')
            for item in app.db.author_set()
        ]

    def get(self):
        return render_template('sitemap.xml', contents=self.get_contents())
