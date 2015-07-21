#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyshorteners.shorteners import Shortener
from quokka import settings


class ShorterURL(object):

    def __init__(self):
        self.shortener = Shortener(settings.SHORTENER_DEFAULT_API)

    def short(self, url):
        return self.shortener.short(url)
