import unittest
import flask
from flask_testing import TestCase  # , Twill
from .flask_csrf_test_client import RequestShim
from quokka import create_app
from quokka.utils import get_current_user_for_models
from quokka.core.admin import create_admin
from flask_wtf.csrf import generate_csrf


class TestCurrentUser(TestCase):
    @classmethod
    def setUpClass(cls):
        '''Set up fixtures for the class.

        This methods runs once for the entire class. This test case do not
        insert or update any record on the database, so there is no problem
        to be run only once for the class.

        This way it save some time, instead of populate the test database
        each time a test is executed.
        '''
        admin = create_admin()
        app = create_app(config='quokka.test_settings',
                         DEBUG=False,
                         test=True,
                         admin_instance=admin)

        with app.app_context():
            db = list(app.extensions.get('mongoengine').keys())[0]
            db.connection.drop_database('quokka_test')
            from quokka.utils.populate import Populate
            Populate(db)()
        cls.app = app
        cls.db = db

    def create_app(self):
        '''Create app must be implemented.

        It is mandatory for flask_testing test cases. Only returns
        the app created in the setUpClass method.
        '''
        return self.app

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
