# coding: utf-8
from flask.ext.testing import TestCase

from quokka import create_app
from flask.ext.security.utils import encrypt_password
from ..models import User


class TestAuthModels(TestCase):
    def setUp(self):
        self.db = self.app.extensions.get('mongoengine')
        self.user_dict = {
            'name': u'Guybrush Treepwood',
            'email': u'guybrush@monkeyisland.com',
            'password': encrypt_password(u'lechucksucks'),
        }
        self.user = User.objects.create(**self.user_dict)

    def tearDown(self):
        User.objects.all().delete()

    def create_app(self):
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True)

    def test_user_fields(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, u'guybrush_monkeyisland_com')
        self.assertEqual(self.user.name, u'Guybrush Treepwood')
        self.assertEqual(self.user.email, u'guybrush@monkeyisland.com')
        self.assertEqual(self.user.password, self.user_dict['password'])
        self.assertEqual(self.user.display_name, self.user.name)
