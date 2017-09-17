from flask import current_app, render_template, abort
from flask.views import MethodView
from .models import make_model


class ArticleListView(MethodView):
    def get(self, category=None):
        limit = current_app.theme_context.get('ARTICLE_LIMIT', 10)
        sort = current_app.theme_context.get(
            'ARTICLE_ORDER_BY', [('date', -1)])

        query = {'published': True}
        if category:
            query['category'] = {'$regex': f"^{category.rstrip('/')}"}

        articles = current_app.db.content_set(query, limit=limit, sort=sort)

        context = {
            'articles': [make_model(article) for article in articles],
            'articles_page': [],
            'HIDE_SIDEBAR': current_app.theme_context.get(
                'HIDE_SIDEBAR_ON_INDEX', False
            )
        }
        if current_app.theme_context.get(
            'SHOW_ABOUT_ME_ON_INDEX', True
        ) is False:
            context['ABOUT_ME'] = None

        if current_app.theme_context.get(
            'SHOW_AVATAR_ON_INDEX', True
        ) is False:
            context['AVATAR'] = None

        return render_template('index.html', **context)


class DetailView(MethodView):
    is_preview = False

    def get(self, slug):
        category, _, slug = slug.rpartition('/')
        content = current_app.db.get_with_content(
            slug=slug,
            category=category
        )
        article = make_model(content)
        if article.status == 'draft' and not self.is_preview:
            abort(404)

        return render_template(
            'article.html',
            article=article,
            category=article.category,
            author=article.author,
            tags=article.tags,
        )


class PreviewView(DetailView):
    # TODO: requires login if login is enabled
    is_preview = True
