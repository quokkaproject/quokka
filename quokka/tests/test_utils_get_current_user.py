import unittest
from flask_testing import TestCase  # , Twill
from .flask_csrf_test_client import FlaskClient
from quokka import create_app
from quokka.utils import get_current_user_for_models
from quokka.core.admin import create_admin


class TestCurrentUser(TestCase):
    def setUp(self):
        self.db = list(self.app.extensions.get('mongoengine').keys())[0]
        self.db.connection.drop_database('quokka_test')
        from quokka.utils.populate import Populate
        Populate(self.db)()
        self.app.test_client_class = FlaskClient
        self.client = self.app.test_client()

    def create_app(self):
        self.admin = create_admin()
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True,
                          admin_instance=self.admin)

    def test_no_one_authenticated(self):
        self.assertIsNone(get_current_user_for_models())

    def test_no_one_authenticated_after_logout(self):
        self.client.login(
            email='author@example.com',
            password='author',
        )
        self.client.logout()
        self.assertIsNone(get_current_user_for_models())

    def test_authenticated_user_should_be_returned(self):
        # app_context request_context test_request_context
        request_context = 'accounts/login/?next=http://localhost/'
        # with self.app.test_request_context(request_context):
        with self.client.application.test_request_context(request_context):
            req = self.client.login(
                email='author@example.com',
                password='author',
            )
            print(req)
            user = get_current_user_for_models()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'author')


if __name__ == '__main__':
    unittest.main()
