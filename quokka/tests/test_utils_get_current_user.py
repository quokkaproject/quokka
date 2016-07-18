import unittest
import flask
from flask_testing import TestCase  # , Twill
from .flask_csrf_test_client import RequestShim
from quokka import create_app
from quokka.utils import get_current_user_for_models
from quokka.core.admin import create_admin
from flask_wtf.csrf import generate_csrf


class TestCurrentUser(TestCase):
    def setUp(self):
        self.db = list(self.app.extensions.get('mongoengine').keys())[0]
        self.db.connection.drop_database('quokka_test')
        from quokka.utils.populate import Populate
        Populate(self.db)()

    def create_app(self):
        self.admin = create_admin()
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True,
                          admin_instance=self.admin)

    @property
    def csrf_token(self):
        request = RequestShim(self.client)
        environ_overrides = {}
        self.client.cookie_jar.inject_wsgi(environ_overrides)
        with self.app.test_request_context(
                "/accounts/login", environ_overrides=environ_overrides,):
            csrf_token = generate_csrf()
            self.app.save_session(flask.session, request)
            return csrf_token

    def login(self, email, password):
        return self.client.post("/accounts/login", data={
            "email": email,
            "password": password,
            "csrf_token": self.csrf_token,
        }, follow_redirects=True)

    def logout(self):
        return self.client.get("/accounts/logout", follow_redirects=True)

    def test_no_one_authenticated(self):
        self.assertIsNone(get_current_user_for_models())

    def test_login_and_logout(self):
        with self.client:
            self.login(
                email='author@example.com',
                password='author',
            )
            user = get_current_user_for_models()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'author')
            self.logout()
            self.assertIsNone(get_current_user_for_models())


if __name__ == '__main__':
    unittest.main()
