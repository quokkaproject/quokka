# coding: utf-8
import sys

from flask.ext.security.utils import encrypt_password

from quokka.core.tests import BaseTestCase
from ..models import User, Role

if sys.version_info.major == 3:
    unicode = lambda x: u'{}'.format(x)  # flake8: noqa


def eval_b(x):
    """Evaluate if to encode the value is necessary.
    """
    if sys.version_info.major == 2:
        return x
    else:
        import codecs
        return codecs.utf_8_encode(x)[0]


class TestAccountsModels(BaseTestCase):
    def setUp(self):
        self.user_dict = {
            'name': u'Guybrush Treepwood',
            'email': u'guybrush@monkeyisland.com',
            'password': encrypt_password(eval_b('lechucksucks')),
        }
        self.role = Role.objects.create(
            name='kill pirates',
            description='hell yeah!'
        )
        self.user = User.objects.create(**self.user_dict)

    def tearDown(self):
        User.objects.all().delete()
        Role.objects.all().delete()

    def test_user_fields(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, u'guybrush-treepwood')
        self.assertEqual(self.user.name, u'Guybrush Treepwood')
        self.assertEqual(self.user.email, u'guybrush@monkeyisland.com')
        self.assertEqual(self.user.password, self.user_dict['password'])
        self.assertEqual(self.user.display_name, self.user.name)
        self.assertEqual(unicode(self.user),
                         'Guybrush Treepwood <guybrush@monkeyisland.com>')

    def test_createuser_classmethod(self):
        user = User.createuser(
            u'Lechuck',
            'lechuck@monkeyisland.com',
            'guybrushsucks',
        )
        self.assertEqual(user.username, u'lechuck')
        self.assertEqual(user.name, u'Lechuck')
        self.assertEqual(user.email, u'lechuck@monkeyisland.com')
        self.assertEqual(user.display_name, user.name)

    def test_generate_username_classmethod(self):
        email = u'elaine.treepwood-ca@monkeyisland.com'
        generated = User.generate_username(email)
        self.assertEqual(generated, u'elaine-treepwood-ca-monkeyisland-com')

    def test_role_field(self):
        self.assertEqual(unicode(self.role.name), u'kill pirates')
        self.assertEqual(unicode(self.role.description), u'hell yeah!')
        self.assertEqual(unicode(self.role), u'kill pirates (hell yeah!)')

    def test_createrole_classmethod(self):
        role = Role.createrole(u'test role', description=u'test description')
        self.assertEqual(role.name, u'test role')
        self.assertEqual(role.description, u'test description')

    def test_user_clean(self):
        self.user.clean()
        self.assertEqual(self.user.username, 'guybrush-treepwood')

    def test_add_role_to_user(self):
        self.user.roles.append(self.role)
        self.assertEqual(self.user.roles.count(), 1)
        self.assertEqual(self.user.roles[0], self.role)
