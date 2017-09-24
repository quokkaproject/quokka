import functools
import logging
import os
from collections import namedtuple
from math import ceil
from flask import current_app as app
import six

logger = logging.getLogger(__name__)
PaginationRule = namedtuple(
    'PaginationRule',
    'min_page URL SAVE_AS',
)

DEFAULT_PP = [(1, '{name}/', '{name}/index{extension}'),
              (2, '{name}/{number}/', '{name}/{number}/index{extension}')]


class Paginator(object):
    def __init__(self, object_list, name=None, settings=None, count=None):
        self.name = name or ''
        self.object_list = object_list
        self.settings = settings or app.theme_context
        self._num_pages = None
        self._count = count

        if self.settings.get('PAGINATION_ENABLED', True):
            self.per_page = self.settings.get('DEFAULT_PAGINATION', 10)
            self.orphans = self.settings.get('DEFAULT_ORPHANS', 0)
        else:
            self.per_page = self.count
            self.orphans = 0

    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.name, self.object_list[bottom:top], number, self,
                    self.settings)

    def _get_count(self):
        "Returns the total number of objects, across all pages."
        if self._count is None:
            self._count = len(self.object_list)
        return self._count
    count = property(_get_count)

    def _get_num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            hits = max(1, self.count - self.orphans)
            self._num_pages = int(ceil(hits / (float(self.per_page) or 1)))
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return list(range(1, self.num_pages + 1))
    page_range = property(_get_page_range)


class Page(object):
    def __init__(self, name, object_list, number, paginator, settings):
        self.name, self.extension = os.path.splitext(name)
        self.object_list = object_list
        self.number = number
        self.paginator = paginator
        self.settings = settings

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.number + 1

    @property
    def next_page(self):
        return self.paginator.page(self.next_page_number())

    def previous_page_number(self):
        return self.number - 1

    @property
    def previous_page(self):
        return self.paginator.page(self.previous_page_number())

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page

    def _from_settings(self, key):
        """Returns URL information as defined in settings. Similar to
        URLWrapper._from_settings, but specialized to deal with pagination
        logic."""

        rule = None

        # find the last matching pagination rule
        pp = self.settings.get('PAGINATION_PATTERNS', DEFAULT_PP)
        for p in [PaginationRule(*r) for r in pp]:
            if p.min_page <= self.number:
                rule = p

        if not rule:
            return ''

        prop_value = getattr(rule, key)

        if not isinstance(prop_value, six.string_types):
            logger.warning('%s is set to %s', key, prop_value)
            return prop_value

        # URL or SAVE_AS is a string, format it with a controlled context
        context = {
            'name': self.name.replace(os.sep, '/'),
            'object_list': self.object_list,
            'number': self.number,
            'paginator': self.paginator,
            'settings': self.settings,
            'base_name': os.path.dirname(self.name),
            'number_sep': '/',
            'extension': f'.{app.config.get("CONTENT_EXTENSION", "html")}',
        }

        if self.number == 1:
            # no page numbers on the first page
            context['number'] = ''
            context['number_sep'] = ''

        ret = prop_value.format(**context)
        if ret[0] == '/':
            ret = ret[1:]
        return ret

    url = property(functools.partial(_from_settings, key='URL'))
    save_as = property(functools.partial(_from_settings, key='SAVE_AS'))
