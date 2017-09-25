from flask import current_app as app, render_template, abort
from flask.views import MethodView
from .models import make_model, make_paginator, Category


def normalize_var(text):
    return text.replace(
        '/', '_'
    ).replace(
        '-', '_'
    ).replace(
        ' ', '_'
    ).replace(
        '@', '_'
    )


class BaseView(MethodView):
    def set_elements_visibility(self, context, content_type):
        """Set elements visibility according to content type
        This works with botstrap3 and malt templates
        Default content_types:
            index, article, page, category, tag, author,
                                  categories, tags, authors
        Custom content types:
            Any category, page or article can be accepted
            `blog/news` or `blog/news/my-article`
        """
        if not content_type:
            return

        CONTENT_TYPE = normalize_var(content_type).upper()

        for rule in app.theme_context.get('DYNAMIC_VARS', []):
            where = rule.get('where')
            var_list = rule.get('var')
            if not where or not var_list:
                continue
            if not isinstance(var_list, list):
                var_list = [var_list]
            if not isinstance(where, list):
                where = [where]
            WHERE = [normalize_var(item).upper() for item in where]
            if CONTENT_TYPE in WHERE:
                for var in var_list:
                    context[var] = rule.get('value', True)


class ArticleListView(BaseView):

    def get(self, category=None, page_number=1):
        context = {}
        query = {'published': True}
        home_template = app.theme_context.get('HOME_TEMPLATE')
        list_categories = app.theme_context.get('LIST_CATEGORIES', [])
        content_type = 'index'
        template = custom_template = 'index.html'
        if category:
            content_type = 'category'
            custom_template = f'{content_type}/{normalize_var(category)}.html'
            if category != app.theme_context.get('CATCHALL_CATEGORY'):
                query['category'] = {'$regex': f"^{category.rstrip('/')}"}
                if category not in list_categories:
                    template = 'category.html'
                else:
                    content_type = 'index'
        elif home_template:
            # use custom template only when categoty is blank '/'
            # and INDEX_TEMPLATE is defined
            template = home_template
            custom_template = f'{content_type}/{home_template}.html'
            content_type = 'home'

        articles = [
            make_model(article)
            for article in app.db.article_set(query)
        ]

        if content_type not in ['index', 'home', 'direct'] and not articles:
            # on `index`, `home` and direct templates no need for articles
            # but category pages should never show empty
            abort(404)

        page_name = category or ''
        paginator = make_paginator(articles, name=page_name)
        page = paginator.page(page_number)

        context.update(
            {
                'articles': articles,
                'page_name': page_name,
                'category': Category(category) if category else None,
                'articles_paginator': paginator,
                'articles_page': page,
                'articles_next_page': page.next_page,
                'articles_previous_page': page.previous_page
            }
        )

        self.set_elements_visibility(context, content_type)
        self.set_elements_visibility(context, category)
        templates = [f'custom/{custom_template}', template]
        print(templates)
        return render_template(templates, **context)


class CategoryListView(BaseView):
    def get(self, page_number=1):
        return 'TODO: a list of categories'


class DetailView(BaseView):
    is_preview = False

    def get(self, slug):
        category, _, item_slug = slug.rpartition('/')
        content = app.db.get_with_content(
            slug=item_slug,
            category=category
        )
        if not content:
            abort(404)

        content = make_model(content)
        if content.status == 'draft' and not self.is_preview:
            abort(404)

        context = {
            'category': content.category,
            'author': content.author,
            content.content_type: content
        }
        if content.author_avatar:
            context['AVATAR'] = content.author_avatar

        self.set_elements_visibility(context, content.content_type)
        self.set_elements_visibility(context, slug)
        templates = [
            f'custom/{content.content_type}/{normalize_var(slug)}.html',
            f'{content.content_type}.html'
        ]
        return render_template(templates, **context)


class PreviewView(DetailView):
    # TODO: requires login if login is enabled
    is_preview = True
