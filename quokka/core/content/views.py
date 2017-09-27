from flask import current_app as app, render_template, abort
from flask.views import MethodView
from .models import make_model, make_paginator, Category, Tag, Author
from quokka.utils.text import slugify_category, normalize_var, slugify


class BaseView(MethodView):
    def set_content_var_map(self, context, content):
        """Export variables from `content` to theme context
        example:
            CONTENT_VAR_MAP:
                author_avatar: AVATAR
        Will get the `article.author_avatar` and export as `AVATAR`

        :param: content must be a `model` of type Content
        """
        MAP = app.theme_context.get('CONTENT_VAR_MAP', {})
        for attr, variable in MAP.items():
            value = getattr(content, attr, None)
            if value is not None:
                context[variable] = value

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
        context['CONTENT_TYPE'] = content_type

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

        # content specific visibility items
        content = context.get('content')
        if content:
            # comments visibility control
            hide = False
            disqus_sitename = app.theme_context.get('DISQUS_SITENAME')

            if 'HIDE_COMMENTS' in app.theme_context:
                hide = app.theme_context['HIDE_COMMENTS']

            if 'HIDE_COMMENTS' in context:
                hide = context['HIDE_COMMENTS']
            else:
                context['HIDE_COMMENTS'] = hide

            if content.comments in ('closed', False):
                hide = True
            elif content.comments in ('opened', True):
                hide = False

            if hide is True:
                context['HIDE_COMMENTS'] = True
                context['DISQUS_SITENAME'] = False
            else:
                context['HIDE_COMMENTS'] = False
                context['DISQUS_SITENAME'] = disqus_sitename


class ArticleListView(BaseView):

    def get(self, category=None, tag=None, author=None, page_number=1):
        context = {}
        query = {'published': True}
        home_template = app.theme_context.get('HOME_TEMPLATE')
        list_categories = app.theme_context.get('LIST_CATEGORIES', [])
        index_category = app.theme_context.get('INDEX_CATEGORY')
        content_type = 'index'
        template = custom_template = 'index.html'

        if category:
            content_type = 'category'
            custom_template = f'{content_type}/{normalize_var(category)}.html'
            if category != index_category:
                query['category_slug'] = {'$regex': f"^{category.rstrip('/')}"}
                if category not in list_categories:
                    template = 'category.html'
                else:
                    content_type = 'index'
            else:
                content_type = 'index'
        elif tag:
            content_type = 'tag'
            custom_template = f'{content_type}/{normalize_var(tag)}.html'
            template = 'tag.html'
            # https://github.com/schapman1974/tinymongo/issues/42
            query['tags_string'] = {'$regex': f'.*,{tag},.*'}
        elif author:
            content_type = 'author'
            custom_template = f'{content_type}/{normalize_var(author)}.html'
            template = 'author.html'
            # https://github.com/schapman1974/tinymongo/issues/42
            author_slugs = author.split('/')
            if len(author_slugs) > 1:
                query['$or'] = [
                    {'authors_string': {'$regex': f'.*,{author_slug},.*'}}
                    for author_slug in author_slugs
                ]
            else:
                query['authors_string'] = {'$regex': f'.*,{author},.*'}
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

        page_name = ''
        if category:
            page_name = category
        elif tag:
            page_name = f'tag/{tag}'
        elif author:
            page_name = f'author/{author}'

        paginator = make_paginator(articles, name=page_name)
        page = paginator.page(page_number)

        context.update(
            {
                'articles': articles,
                'page_name': page_name,
                'category': Category(category) if category else None,
                'tag': Tag(tag) if tag else None,
                'author': Author(author) if author else None,
                'articles_paginator': paginator,
                'articles_page': page,
                'articles_next_page': page.next_page,
                'articles_previous_page': page.previous_page
            }
        )

        self.set_elements_visibility(context, content_type)
        self.set_elements_visibility(context, category)
        templates = [f'custom/{custom_template}', template]
        return render_template(templates, **context)


class CategoryListView(BaseView):
    def get(self):
        # TODO: Split categories by `/` to get roots
        categories = [
            (
                Category(cat),
                [
                    make_model(article)
                    for article in app.db.article_set(
                        {'category_slug': slugify_category(cat),
                         'published': True}
                    )
                ]
            )
            for cat in app.db.value_set(
                'index', 'category',
                filter={'published': True},
                sort=True
            )
        ]

        context = {
            'categories': categories
        }

        self.set_elements_visibility(context, 'categories')
        return render_template('categories.html', **context)


class TagListView(BaseView):
    def get(self, page_number=1):
        tags = [
            (Tag(tag), [])
            for tag in app.db.tag_set(filter={'published': True})
        ]
        context = {'tags': tags}
        self.set_elements_visibility(context, 'tags')
        return render_template('tags.html', **context)


class AuthorListView(BaseView):
    def get(self):
        authors = [
            (
                Author(author),
                [
                    make_model(article)
                    for article in app.db.article_set(
                        {'authors_string': {
                            '$regex': f'.*,{slugify(author)},.*'},
                         'published': True}
                    )
                ]
            )
            for author in app.db.author_set(filter={'published': True})
        ]

        context = {
            'authors': authors
        }

        self.set_elements_visibility(context, 'authors')
        return render_template('authors.html', **context)


class DetailView(BaseView):
    is_preview = False

    def get(self, slug):
        category, _, item_slug = slug.rpartition('/')
        content = app.db.get_with_content(
            slug=item_slug,
            category_slug=category
        )
        if not content:
            abort(404)

        content = make_model(content)
        if content.status == 'draft' and not self.is_preview:
            abort(404)

        context = {
            'category': content.category,
            'author': content.author,
            'content': content,
            content.content_type: content
        }

        self.set_elements_visibility(context, content.content_type)
        self.set_elements_visibility(context, slug)
        self.set_content_var_map(context, content)
        templates = [
            f'custom/{content.content_type}/{normalize_var(slug)}.html',
            f'{content.content_type}.html'
        ]
        return render_template(templates, **context)


class PreviewView(DetailView):
    # TODO: requires login if login is enabled
    is_preview = True
