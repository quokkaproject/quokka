import functools
from .utils import url_for_content, url_for_category
from .formats import get_format
from .paginator import Paginator
from flask import current_app as app
from quokka.utils.text import slugify


@functools.total_ordering
class Orderable:
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.slug == other.slug
        if isinstance(other, str):
            return self.slug == self._normalize_key(other)
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.slug != other.slug
        if isinstance(other, str):
            return self.slug != self._normalize_key(other)
        return True

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.slug < other.slug
        if isinstance(other, str):
            return self.slug < self._normalize_key(other)
        return False

    def __hash__(self):
        return hash(self.slug)

    def _normalize_key(self, key):
        return slugify(key)

    def __html__(self):
        return str(self)


class Series(Orderable):
    def __init__(self, name, index=1):
        self.name = self.slug = name
        self._index = index

    @property
    def index(self):
        return self._index

    @property
    def next(self):
        return []

    @property
    def previous(self):
        return []

    @property
    def all(self):
        return []

    @property
    def all_previous(self):
        return []

    @property
    def all_next(self):
        return []


class Category:
    def __init__(self, category):
        self.category = self.name = self.slug = category

    @property
    def url(self):
        return url_for_category(self.category)

    def __str__(self):
        return self.category


class Author:
    def __init__(self, authors):
        self.authors = authors

    @property
    def name(self):
        return ', '.join(self.authors)

    @property
    def social(self):
        # twitter: ...
        return {}

    @property
    def url(self):
        authors_list = '/'.join(
            slugify(author) for author in self.authors
        )
        return f'authors/{authors_list}'

    def __str__(self):
        return self.name


class Tag(Orderable):
    def __init__(self, name):
        self.name = self.slug = name

    @property
    def url(self):
        # TODO: implement
        return f'tag/{self.name}.html'

    def __str__(self):
        return self.name

    def __getitem__(self, item):
        return self


class Content:
    def __init__(self, data):
        self.data = data
        self.format = get_format(data)

    @property
    def url(self):
        return url_for_content(self)

    @property
    def locale_date(self):
        # TODO: format according to settings
        return self.data['date'].isoformat()

    @property
    def locale_modified(self):
        # TODO: format according to settings
        return self.data['modified'].isoformat()

    @property
    def metadata(self):
        # TODO: get metadata from database
        # TODO: implement libratar/gravatar
        return {
           # 'cover': 'foo',
           # 'author_gravatar': 'http://i.pravatar.cc/300',
           # 'about_author': 'About Author',
           # 'translations': ['en'],
           # 'og_image': 'foo',
           # 'series': 'aa',
           # 'asides': 'aaa'
        }

    @property
    def author_gravatar(self):
        return self.author_avatar

    @property
    def author_avatar(self):
        return self.metadata.get(
            'author_avatar',
            app.theme_context.get(
                'AVATAR',
                'http://i.pravatar.cc/300'
            )
        )

    @property
    def summary(self):
        return self.data.get('summary') or ''

    @property
    def header_cover(self):
        return None

    @property
    def header_color(self):
        return None

    @property
    def sidebar(self):
        return True

    @property
    def use_schema_org(self):
        return True

    @property
    def comments(self):
        return 'True'

    @property
    def status(self):
        return "draft" if not self.data.get('published') else "published"

    @property
    def lang(self):
        return self.data.get('language')

    @property
    def author(self):
        if self.data.get('authors'):
            return Author(self.data['authors'])

    @property
    def related_posts(self):
        # TODO: depends on CONTENT_ADD_RELATED_POSTS
        return []

    @property
    def banner(self):
        # TODO: get it from model
        return 'http://lorempixel.com/1000/200/abstract/'

    @property
    def image(self):
        return self.banner

    @property
    def series(self):
        # https://github.com/getpelican/pelican-plugins/tree/master/series
        return Series('foo')

    @property
    def content(self):
        return self.format.render(self.data) or ''

    @property
    def category(self):
        return Category(self.data['category'])

    @property
    def tags(self):
        return [Tag(tag) for tag in self.data.get('tags', [])]

    @property
    def keywords(self):
        return self.tags

    @property
    def description(self):
        return self.summary

    @property
    def menulabel(self):
        return self.title

    def __getattr__(self, attr):
        value = self.metadata.get(attr) or self.data.get(attr)
        if not value:
            raise AttributeError(f'{self} do not have {attr}')
        return value

    def __str__(self):
        return self.data['title']

    def __html__(self):
        return str(self)


class Article(Content):
    pass


class Page(Content):
    pass


def make_model(content):
    if isinstance(content, Content):
        return content

    if content['content_type'] == 'article':
        return Article(content)
    elif content['content_type'] == 'page':
        return Page(content)

    return Content(content)


def make_paginator(object_list, *args, **kwargs):
    object_list = [
        obj if isinstance(obj, Content) else make_model(obj)
        for obj
        in object_list
    ]
    return Paginator(object_list, *args, **kwargs)
