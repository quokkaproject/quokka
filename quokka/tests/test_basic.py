import unittest
from flask.ext.testing import TestCase  # , Twill
from quokka import create_app
from quokka.core.admin import create_admin


class BasicTestCase(TestCase):

    def setUp(self):
        self.db = list(self.app.extensions.get('mongoengine').keys())[0]
        self.db.connection.drop_database('quokka_test')
        from quokka.utils.populate import Populate
        Populate(self.db)()

    def login(self, username, password):
        return self.app.post('/accounts/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/accounts/logout', follow_redirects=True)

    def get_config(self, key):
        return self.app.config.store.get(key)

    def create_app(self):
        self.admin = create_admin()
        return create_app(config='quokka.test_settings',
                          DEBUG=False,
                          test=True,
                          admin_instance=self.admin)

    def test_has_mongoengine(self):
        self.assertTrue(self.app.extensions.get('mongoengine'))

    def test_db_is_connected_in_the_test_database(self):
        self.assertTrue(
            self.db.connection.PORT == self.get_config('MONGODB_PORT')
        )
        self.assertTrue(
            self.db.connection.HOST == self.get_config('MONGODB_HOST')
        )

    def test_has_posts(self):
        from quokka.modules.posts.models import Post
        self.assertTrue(Post.objects.count() in [5, 6])

    def test_blog_has_only_one_post(self):
        from quokka.modules.posts.models import Post
        only_blog_filter = {'__raw__': {'mpath': {'$regex': '^,blog,'}}}
        self.assertTrue(Post.objects(**only_blog_filter).count() == 1)

    def test_blog_including_related_has_only_3_posts(self):
        from quokka.modules.posts.models import Post
        only_blog_filter = {
            '__raw__': {
                '$or': [
                    {'mpath': {'$regex': '^,blog,'}},
                    {'related_mpath': {'$regex': '^,blog,'}}
                ]
            }
        }
        self.assertTrue(Post.objects(**only_blog_filter).count() == 3)

    def test_has_default_theme(self):
        from quokka.core.models import Config
        self.assertTrue(Config.get('settings', 'DEFAULT_THEME') == 'pure')

    def test_app_has_admin(self):
        self.assertTrue(self.app.extensions.get("admin"))

    # def test_admin_requires_password(self):
    #     t = Twill(self.app)
    #     with t:
    #         url = t.url('/admin')
    #         t.browser.go(url)
    #         import ipdb
    #         ipdb.set_trace()
    #         self.assertTrue('login' in t.browser.result.page)


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
