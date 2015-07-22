#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyshorteners.shorteners import Shortener
from quokka.utils.settings import get_setting_value


class ShorterURL(object):

    _shortener = None

    @property
    def shortener(self):
        if not self._shortener:
            shortener_name = get_setting_value('SHORTENER_DEFAULT_API')
            self._shortener = Shortener(shortener_name)
        return self._shortener

    def short(self, url):
        return self.shortener.short(url)
