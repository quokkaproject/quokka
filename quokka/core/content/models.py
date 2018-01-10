import functools
from .utils import url_for_content
from .formats import get_format
from .paginator import Paginator
from flask import url_for
from flask import current_app as app
from quokka.utils.text import (
    slugify, slugify_category, make_social_link,
    make_social_name, make_external_url
)
from quokka.utils.dateformat import pretty_date
from quokka.utils.custom_vars import custom_var_dict


DEFAULT_DATE_FORMAT = '%a %d %B %Y'


@functools.total_ordering
class Orderable:

    is_content = False  # to use in templates

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

    @property
    def external_url(self):
        return make_external_url(self.url)


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


class Category(Orderable):
    def __init__(self, category):
        self.category = category
        self.slug = slugify_category(category)
        if category == self.slug:
            self.name = category.replace('-', ' ').title()
        else:
            self.name = category

    @property
    def url(self):
        return self.slug

    def __str__(self):
        return self.category


class Fixed(Orderable):
    """Fixed pages like /authors/ and /tags/ and /categories/"""
    def __init__(self, name):
        self.name = name
        self.slug = slugify_category(name)

    @property
    def url(self):
        return self.slug

    def __str__(self):
        return self.name


class Url(Fixed):
    """For compatibility"""

    def __init__(self, name):
        self.name = name
        self.slug = name


class Author(Orderable):
    def __init__(self, authors):
        self.authors = authors
        self._profile_page = 'empty'

    @property
    def name(self):
        if isinstance(self.authors, str):
            return self.authors.replace('-', ' ').replace('/', ' & ').title()
        elif isinstance(self.authors, (list, tuple)):
            return ', '.join(self.authors)

    @property
    def slug(self):
        if isinstance(self.authors, str):
            return slugify(self.authors)
        if len(self.authors) > 1:
            return '/'.join(
                slugify(author) for author in self.authors
            )
        else:
            return slugify(self.authors[0])

    @property
    def social(self):
        # twitter: ...
        return {}

    @property
    def url(self):
        return f'author/{self.slug}'

    def __str__(self):
        return self.name

    @property
    def profile_page(self):
        if self._profile_page == 'empty':
            profile = app.db.get(
                'index',
                {'content_type': 'block',
                 'slug': self.slug,
                 'published': True}
            )
            if profile:
                self._profile_page = Block(profile)
            else:
                self._profile_page = None
        return self._profile_page


class Tag(Orderable):
    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)

    @property
    def url(self):
        return f'tag/{self.slug}/index.html'

    def __str__(self):
        return self.name

    def __getitem__(self, item):
        return self


class Content:

    is_content = True  # to use in templates

    def __init__(self, data):
        self.data = data
        self.format = get_format(data)

    @property
    def url(self):
        return url_for_content(self)

    @property
    def external_url(self):
        return make_external_url(self.url)

    @property
    def locale_date(self):
        if app.theme_context.get('SHOW_PRETTY_DATES') is True:
            return pretty_date(self.data['date'])
        date_format = app.theme_context.get(
            'DEFAULT_DATE_FORMAT', DEFAULT_DATE_FORMAT
        )
        return self.data['date'].strftime(date_format)

    @property
    def locale_modified(self):
        if app.theme_context.get('SHOW_PRETTY_DATES') is True:
            return pretty_date(self.data['modified'])
        date_format = app.theme_context.get(
            'DEFAULT_DATE_FORMAT', DEFAULT_DATE_FORMAT
        )
        return self.data['modified'].strftime(date_format)

    @property
    def metadata(self):
        # TODO: get metadata from database
        # TODO: implement libratar/gravatar
        # return {
            # 'cover': 'foo',
            # 'author_gravatar': 'http://i.pravatar.cc/300',
            # 'about_author': 'About Author',
            # 'translations': ['en'],
            # 'og_image': 'foo',
            # 'series': 'aa',
            # 'asides': 'aaa'
        # }
        data = {}
        data.update(custom_var_dict(self.data.get('custom_vars')))
        return data

    @property
    def author_gravatar(self):
        return self.author_avatar

    @property
    def author_avatar(self):
        if self.author.profile_page:
            return self.author.profile_page.author_avatar
        return self.metadata.get(
            'author_avatar',
            app.theme_context.get(
                'AVATAR',
                'https://api.adorable.io/avatars/250/quokkacms.png'
            )
        )

    @property
    def summary(self):
        # return self.metadata.get('summary') or self.data.get('summary') or ''
        return self.get('summary', '')

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
        # data = self.data.get('comments', None)
        # if data is not None:
        #     return data or 'closed'
        return "closed" if not self.data.get('comments') else "opened"

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
        # return 'http://lorempixel.com/1000/600/abstract/'
        return url_for('theme_static', filename='img/island.jpg')

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

    @property
    def name(self):
        return self.title

    def __getattr__(self, attr):
        value = self.metadata.get(attr) or self.data.get(attr)
        if not value:
            raise AttributeError(f'{self} do not have {attr}')
        return value

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        for name in ['title', 'name', '_id']:
            if self.data.get(name):
                return self.data[name]
        return str(self.__class__)

    def __html__(self):
        return str(self)

    def get(self, name, *args, **kwargs):
        return self.metadata.get(
            name
        ) or self.data.get(
            name, *args, **kwargs
        )


class Article(Content):
    """Represents dated authored article"""


class Page(Content):
    """Represents a static page"""


class Block(Content):
    """Represents a block of items"""

    @property
    def block_items(self):
        return [
            make_model(item) for item in self.data['block_items']
        ]

    @property
    def author_avatar(self):
        if self.metadata.get('gravatar_email'):
            return f"https://avatars.io/gravatar/{make_social_name(self.metadata.get('gravatar_email'))}"  # noqa
        if self.metadata.get('twitter'):
            return f"https://avatars.io/twitter/{make_social_name(self.metadata.get('twitter'))}"  # noqa
        if self.metadata.get('facebook'):
            return f"https://avatars.io/facebook/{make_social_name(self.metadata.get('facebook'))}"  # noqa
        if self.metadata.get('instagram'):
            return f"https://avatars.io/instagram/{make_social_name(self.metadata.get('instagram'))}"  # noqa
        return self.metadata.get(
            'author_avatar',
            f'https://api.adorable.io/avatars/250/{self.slug}.png'
        )

    @property
    def social_links(self):
        links = []
        for social, social_link in app.theme_context.get('SOCIALNETWORKS', []):
            link = self.metadata.get(social)
            if link:
                links.append((social, make_social_link(social_link, link)))
        return links


class BlockItem(Content):
    """Represents an item inside a block"""

    @property
    def is_block(self):
        return isinstance(self.item, Block)

    @property
    def is_dropdown(self):
        return self.item_type == 'dropdown'

    @property
    def item(self):
        if self.metadata.get('index_id') or self.data.get('index_id'):
            return make_model(app.db.get('index', {'_id': self.index_id}))
        for ref in ['author', 'category', 'tag', 'url']:
            data = self.data.get(f"{ref}_id")
            if data:
                return make_model(data, ref)
        return self.metadata.get('item') or self.data.get('item')

    @property
    def name(self):
        given_name = self.metadata.get('name') or self.data.get('name')
        given_title = self.metadata.get('title')
        try:
            item_name = self.item.name
        except AttributeError:
            item_name = self.item

        return given_name or given_title or item_name

    @property
    def url(self):
        try:
            return self.item.url
        except AttributeError:
            return self.data['item']


def make_model(content, content_type=None):
    if isinstance(content, Content):
        return content
    content_type = content_type or content.get('content_type', 'content')
    words = [word.capitalize() for word in content_type.lower().split('_')]
    model_name = ''.join(words)
    return globals().get(model_name, Content)(content)


def make_paginator(object_list, *args, **kwargs):
    object_list = [
        obj if isinstance(obj, Content) else make_model(obj)
        for obj
        in object_list
    ]
    return Paginator(object_list, *args, **kwargs)
