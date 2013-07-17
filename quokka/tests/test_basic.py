import unittest
from flask.ext.testing import TestCase, Twill
from quokka import create_app
from quokka.core.admin import create_admin


class BasicTestCase(TestCase):

    def login(self, username, password):
        return self.app.post('/accounts/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/accounts/logout', follow_redirects=True)

    def get_config(self, key):
        return self.app.config.get(key)

    def create_app(self):
        self.admin = create_admin()
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True,
                          admin_instance=self.admin)

    def test_has_mongoengine(self):
        self.assertTrue(self.app.extensions.get('mongoengine'))

    def test_db_is_connected_in_the_test_database(self):
        db = self.app.extensions.get('mongoengine')
        dbconf = self.get_config('MONGODB_SETTINGS')
        self.assertTrue(
            db.connection.port == dbconf.get('PORT', 27017)
        )
        self.assertTrue(
            db.connection.host == dbconf.get('HOST', 'localhost')
        )

    def test_app_has_admin(self):
        self.assertTrue(self.app.extensions.get("admin"))

    def test_admin_requires_password(self):
        t = Twill(self.app)
        with t:
            url = t.url('/admin')
            t.browser.go(url)
            self.assertTrue('login' in t.browser.result.page)


if __name__ == '__main__':
    unittest.main()


"""
Twill.browser
['back', 'cj', 'clear_cookies',
'clicked', 'creds', 'find_link',
'follow_link', 'get_all_forms',
'get_code', 'get_form',
'get_form_field', 'get_html',
'get_title', 'get_url', 'go',
'last_submit_button', 'load_cookies',
'reload', 'result', 'save_cookies', 'set_agent_string',
'show_cookies', 'showforms', 'showhistory',
'showlinks', 'submit']
"""
