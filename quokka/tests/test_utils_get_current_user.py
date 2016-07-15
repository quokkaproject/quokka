import unittest
from flask_testing import TestCase  # , Twill
from quokka import create_app
from quokka.utils import get_current_user_for_models
from quokka.modules.accounts.models import User


class TestCurrentUser(TestCase):
    def setUp(self):
        self.db = list(self.app.extensions.get('mongoengine').keys())[0]
        self.db.connection.drop_database('quokka_test')
        user = User.createuser(
            u'author',
            'author@example.com',
            password='author',
        )


    def create_app(self):
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True)

    def login(self, username, password):
        return self.client.post('/accounts/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/accounts/logout', follow_redirects=True)

    def test_no_one_authenticated(self):
        with self.app.test_request_context():
            self.assertIsNone(get_current_user_for_models())

    def test_no_one_authenticated_after_logout(self):
        with self.app.test_request_context():
            self.login('author', 'author')
            self.logout()
            self.assertIsNone(get_current_user_for_models())

    def test_authenticated_user_should_be_returned(self):
        with self.app.test_request_context():
            self.login('author', 'author')
            user = get_current_user_for_models()
            self.assertIsNotNone(user)
            self.assertIsEqual(user.name, 'author')


if __name__ == '__main__':
    unittest.main()
