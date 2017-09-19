from flask import current_app as app, render_template, abort
from flask.views import MethodView
from .models import make_model, make_paginator


class ArticleListView(MethodView):
    def get(self, category=None, page_number=1):
        query = {'published': True}
        if category:
            query['category'] = {'$regex': f"^{category.rstrip('/')}"}

        articles = [
            make_model(article)
            for article in app.db.content_set(query)
        ]

        page_name = f'category/{category}' if category else 'index'
        paginator = make_paginator(articles, name=page_name)
        page = paginator.page(page_number)

        context = {
            'articles': articles,
            'page_name': page_name,
            'articles_paginator': paginator,
            'articles_page': page,
            'articles_next_page': page.next_page,
            'articles_previous_page': page.previous_page,
            'HIDE_SIDEBAR': app.theme_context.get(
                'HIDE_SIDEBAR_ON_INDEX', False
            )
        }

        if app.theme_context.get(
            'SHOW_ABOUT_ME_ON_INDEX', True
        ) is False:
            context['ABOUT_ME'] = None

        if app.theme_context.get(
            'SHOW_AVATAR_ON_INDEX', True
        ) is False:
            context['AVATAR'] = None

        if app.theme_context.get('HIDE_SIDEBAR_ON_INDEX'):
            context['HIDE_SIDEBAR'] = True

        if app.theme_context.get('SIDEBAR_ON_LEFT_ON_INDEX'):
            context['SIDEBAR_ON_LEFT'] = True

        return render_template('index.html', **context)


class CategoryListView(MethodView):
    def get(self, page_number=1):
        return 'TODO: a list of categories'


class DetailView(MethodView):
    is_preview = False

    def get(self, slug):
        category, _, slug = slug.rpartition('/')
        content = app.db.get_with_content(
            slug=slug,
            category=category
        )
        article = make_model(content)
        context = {
            'article': article,
            'category': article.category,
            'tags': article.tags,
            'author': article.author
        }

        if article.status == 'draft' and not self.is_preview:
            abort(404)

        if app.theme_context.get('DISPLAY_RECENT_POSTS_ON_SIDEBAR'):
            context['articles'] = [
                make_model(item)
                for item in app.db.content_set({'published': True})
            ]

        if app.theme_context.get('HIDE_SIDEBAR_ON_ARTICLE'):
            context['HIDE_SIDEBAR'] = True

        if app.theme_context.get('SIDEBAR_ON_LEFT_ON_ARTICLE'):
            context['SIDEBAR_ON_LEFT'] = True

        if article.author_avatar:
            content['AVATAR'] = article.author_avatar

        return render_template('article.html', **context)


class PreviewView(DetailView):
    # TODO: requires login if login is enabled
    is_preview = True
