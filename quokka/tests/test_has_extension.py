import unittest
from quokka import create_app


class HasExtensionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def test_app_has_admin(self):
        self.assertTrue(self.app.extensions.get("admin"))

    def test_app_has_mongoengine(self):
        self.assertTrue(self.app.extensions.get("mongoengine"))

if __name__ == '__main__':
    unittest.main()
