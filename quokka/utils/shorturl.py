#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyshorteners.shorteners import Shortener
from quokka.utils.settings import get_setting_value


class ShorterURL(object):

    __shortener = None

    @property
    def shortener(self):
        if not self.__shortener:
            shortener_config = get_setting_value(
                'SHORTENER_SETTINGS', {}).copy()
            shortener_name = shortener_config.pop('name')
            self.__shortener = Shortener(shortener_name, **shortener_config)
        return self.__shortener

    def short(self, url):
        url = url.replace('localhost', '127.0.0.1')
        return self.shortener.short(url)
