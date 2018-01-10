import hashlib
import PyRSS2Gen as pyrss
from datetime import datetime, timedelta
from flask import current_app as app, render_template, abort, request
from flask.views import MethodView

# from werkzeug.contrib.atom import AtomFeed
# The werkzeug AtomFeed escapes all html tags
from quokka.utils.atom import AtomFeed

from .models import make_model, make_paginator, Category, Tag, Author
from quokka.utils.text import (
    slugify_category, normalize_var, slugify, cdata, make_external_url
)


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

    def get(self, category=None, tag=None, author=None,
            page_number=1, ext=None):
        context = {}
        query = {'published': True}
        home_template = app.theme_context.get('HOME_TEMPLATE')
        list_categories = app.theme_context.get('LIST_CATEGORIES', [])
        index_category = app.theme_context.get('INDEX_CATEGORY')
        content_type = 'index'
        template = custom_template = 'index.html'
        ext = ext or app.config.get('CONTENT_EXTENSION', 'html')
        FEED_ALL_ATOM = app.theme_context.get('FEED_ALL_ATOM')
        FEED_ALL_RSS = app.theme_context.get('FEED_ALL_RSS')

        if category:
            FEED_ALL_ATOM = f"{category}/index.atom"
            FEED_ALL_RSS = f"{category}/index.rss"
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
            FEED_ALL_ATOM = f"tag/{tag}/index.atom"
            FEED_ALL_RSS = f"tag/{tag}/index.rss"
            content_type = 'tag'
            custom_template = f'{content_type}/{normalize_var(tag)}.html'
            template = 'tag.html'
            # https://github.com/schapman1974/tinymongo/issues/42
            query['tags_string'] = {'$regex': f'.*,{tag},.*'}
        elif author:
            FEED_ALL_ATOM = f"author/{author}/index.atom"
            FEED_ALL_RSS = f"author/{author}/index.rss"
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
                'articles_previous_page': page.previous_page,
                'FEED_ALL_ATOM': FEED_ALL_ATOM,
                'FEED_ALL_RSS': FEED_ALL_RSS
            }
        )

        self.set_elements_visibility(context, content_type)
        self.set_elements_visibility(context, category)
        templates = [f'custom/{custom_template}', template]

        return self.render(ext, content_type, templates, **context)

    def render(self, ext, content_type, templates, **context):
        extension_map = app.config.get('CONTENT_EXTENSION_MAP', {})
        method_name = extension_map.get(ext, 'render_template')
        return getattr(self, method_name)(content_type, templates, **context)

    def render_template(self, content_type, templates, **context):
        return render_template(templates, **context)

    def render_atom(self, content_type, templates, **context):
        feed_name = (
            f"{app.theme_context.get('SITENAME')}"
            f" | {content_type.title()} | atom feed"
        )
        if context.get('articles_page'):
            contents = context['articles_page'].object_list
        else:
            contents = context['articles']

        feed = AtomFeed(
            feed_name,
            feed_url=request.url,
            url=request.url_root
        )
        for content in contents:
            content = make_model(content)
            feed.add(
                content.title,
                cdata(content.content),
                content_type="html",
                author=content.author,
                url=make_external_url(content.url),
                updated=content.modified,
                published=content.date
            )
        return feed.get_response()

    def render_rss(self, content_type, templates, **context):

        feed_name = description = (
            f"{app.theme_context.get('SITENAME')}"
            f" | {content_type.title()} | RSS feed"
        )

        if context.get('articles_page'):
            contents = context['articles_page'].object_list
        else:
            contents = context['articles']

        rss = pyrss.RSS2(
            title=feed_name,
            link=request.url_root,
            description=description,
            language=app.config.get('RSS_LANGUAGE', 'en-us'),
            copyright=app.config.get('RSS_COPYRIGHT', 'All rights reserved.'),
            lastBuildDate=datetime.now(),
            categories=[str(context.get('tag') or context.get('category'))],
        )

        # set rss.pubDate to the newest post in the collection
        # back 10 years in the past
        rss_pubdate = datetime.today() - timedelta(days=365 * 10)

        for content in contents:
            content = make_model(content)

            if content.date > rss_pubdate:
                rss_pubdate = content.date

            rss.items.append(
                pyrss.RSSItem(
                    title=content.title,
                    link=make_external_url(content.url),
                    description=cdata(content.content),
                    author=str(content.author),
                    categories=[str(content.tags)],
                    guid=hashlib.sha1(
                        content.title.encode('utf-8') +
                        content.url.encode('utf-8')
                    ).hexdigest(),
                    pubDate=content.date,
                )
            )

        # set the new published date after iterating the contents
        rss.pubDate = rss_pubdate

        return rss.to_xml(encoding=app.config.get('RSS_ENCODING', 'utf-8'))


class CategoryListView(BaseView):

    def build_query(self, cat):
        query = {'published': True}
        if cat == app.theme_context.get('INDEX_CATEGORY', 'index'):
            return query
        if cat:
            query['category_slug'] = {
                '$regex': f"^{slugify_category(cat).rstrip('/')}"
            }
        else:
            query['category_slug'] = cat
        return query

    def get(self, ext=None):
        categories = [
            (
                Category(cat),
                [
                    make_model(article)
                    for article in app.db.article_set(self.build_query(cat))
                ]
            )
            for cat in app.db.category_set(
                filter={'published': True}
            ) + ['index']
        ]
        context = {
            'categories': categories
        }

        self.set_elements_visibility(context, 'categories')
        return render_template('categories.html', **context)


class TagListView(BaseView):
    def get(self, page_number=1, ext=None):
        tags = [
            (Tag(tag), [])
            for tag in app.db.tag_set(filter={'published': True})
        ]
        context = {'tags': tags}
        self.set_elements_visibility(context, 'tags')
        return render_template('tags.html', **context)


class AuthorListView(BaseView):
    def get(self, ext=None):
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

    def get(self, slug, ext=None):
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
