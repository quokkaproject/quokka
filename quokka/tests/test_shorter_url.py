#!/usr/bin/env python
# coding: utf-8

import unittest
from quokka.utils.shorturl import ShorterURL


class TestShorterUrl(unittest.TestCase):

    def test_usage(self):
        url = 'http://google.com'

        shorter = ShorterURL()
        self.assertIsNotNone(shorter)
        self.assertIsNotNone(shorter.short(url))
