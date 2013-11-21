# coding: utf-8
from flask.ext.testing import TestCase

from quokka import create_app
from quokka.core.admin import create_admin


class BaseTestCase(TestCase):
    def create_app(self):
        self.admin = create_admin()
        return create_app(config='quokka.test_settings',
                          admin_instance=self.admin,
                          test=True)
