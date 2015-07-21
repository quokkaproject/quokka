#!/usr/bin/env python
# coding: utf-8

import unittest
from quokka.utils.shorturl import ShorterURL
from quokka import create_app


class TestShorterUrl(unittest.TestCase):
    def create_app(self):
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True)

    def test_usage(self):
        url = 'http://google.com'
        app = self.create_app()
        with app.app_context():
            shorter = ShorterURL()
            self.assertIsNotNone(shorter)
            self.assertIsNotNone(shorter.short(url))
