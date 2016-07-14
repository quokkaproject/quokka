import unittest
from flask_testing import TestCase
from quokka import create_app
from quokka.core.admin import create_admin
from quokka.utils.populate import Populate


class PopulateTestCase(TestCase):
    def setUp(self):
        self.db = list(self.app.extensions.get('mongoengine').keys())[0]
        self.db.connection.drop_database('quokka_test')
        self.populate = Populate(self.db)

    def create_app(self):
        self.admin = create_admin()
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True,
                          admin_instance=self.admin)

    def test_role_called_with_name_and_instance(self):
        role_1st_call = self.populate.role('admin')
        role_2nd_call = self.populate.role(role_1st_call)
        self.assertEqual(role_1st_call.name, role_2nd_call.name)


if __name__ == '__main__':
    unittest.main()
