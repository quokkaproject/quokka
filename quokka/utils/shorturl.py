#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyshorteners.shorteners import Shortener
from quokka.utils import lazy_str_setting


class ShorterURL(object):

    _shortener = None

    @property
    def shortener(self):
        if not self._shortener:
            shortener_name = lazy_str_setting('SHORTENER_DEFAULT_API')
            self._shortener = Shortener(shortener_name)
        return self._shortener

    def short(self, url):
        return self.shortener.short(url)
