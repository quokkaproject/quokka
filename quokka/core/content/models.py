import functools
import six
from .utils import url_for_content, url_for_category
from .formats import get_format
from quokka.utils.text import slugify


@functools.total_ordering
class Orderable:
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.slug == other.slug
        if isinstance(other, six.text_type):
            return self.slug == self._normalize_key(other)
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.slug != other.slug
        if isinstance(other, six.text_type):
            return self.slug != self._normalize_key(other)
        return True

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.slug < other.slug
        if isinstance(other, six.text_type):
            return self.slug < self._normalize_key(other)
        return False

    def __hash__(self):
        return hash(self.slug)

    def _normalize_key(self, key):
        return six.text_type(slugify(key))


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
        self.category = self.slug = category

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
    def url(self):
        # TODO: implement
        # if multiple generate authors/post_lug
        # if single generate author/authorslug
        return f'author/{slugify(self.authors[0])}'

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
        return self.data['date']

    @property
    def metadata(self):
        # TODO: get metadata from database
        # TODO: implement libratar/gravatar
        return {
           # 'cover': 'foo',
           'author_gravatar': 'http://i.pravatar.cc/300',
           # 'about_author': 'About Author',
           # 'translations': ['en'],
           # 'og_image': 'foo',
           # 'series': 'aa',
           # 'asides': 'aaa'
        }

    @property
    def lang(self):
        return self.data.get('language')

    @property
    def author(self):
        return Author(self.data['authors'])

    @property
    def related_posts(self):
        # TODO: depends on CONTENT_ADD_RELATED_POSTS
        return []

    @property
    def series(self):
        # https://github.com/getpelican/pelican-plugins/tree/master/series
        return Series('foo')

    @property
    def content(self):
        return self.format.render_content(self.data)

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
        return [self.summary]

    def __getattr__(self, attr):
        return self.metadata.get(attr) or self.data.get(attr, '')


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
