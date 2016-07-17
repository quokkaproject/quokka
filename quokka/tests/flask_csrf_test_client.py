# Want to run your Flask tests with CSRF protections turned on, to make sure
# that CSRF works properly in production as well? Here's an excellent way
# to do it!

# Adapted from:
# https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
#
# First some imports. I'm assuming you're using Flask-WTF for CSRF protection.
import flask
from flask.testing import FlaskClient as BaseFlaskClient
from flask_wtf.csrf import generate_csrf


# Flask's assumptions about an incoming request don't quite match up with
# what the test client provides in terms of manipulating cookies, and the
# CSRF system depends on cookies working correctly. This little class is a
# fake request that forwards along requests to the test client for setting
# cookies.
class RequestShim(object):
    """
    A fake request that proxies cookie-related methods to a Flask test client.
    """
    def __init__(self, client):
        self.client = client

    def set_cookie(self, key, value='', *args, **kwargs):
        "Set the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.set_cookie(
            server_name, key=key, value=value, *args, **kwargs
        )

    def delete_cookie(self, key, *args, **kwargs):
        "Delete the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.delete_cookie(
            server_name, key=key, *args, **kwargs
        )


# We're going to extend Flask's built-in test client class, so that it knows
# how to look up CSRF tokens for you!
class FlaskClient(BaseFlaskClient):
    @property
    def csrf_token(self):
        # First, we'll wrap our request shim around the test client, so that
        # it will work correctly when Flask asks it to set a cookie.
        request = RequestShim(self)
        # Next, we need to look up any cookies that might already exist on
        # this test client, such as the secure cookie that powers
        # `flask.session`, and make a test request context that has
        # those cookies in it.
        environ_overrides = {}
        self.cookie_jar.inject_wsgi(environ_overrides)
        with flask.current_app.test_request_context(
                "/accounts/login", environ_overrides=environ_overrides,):
            # Now, we call Flask-WTF's method of generating a CSRF token...
            csrf_token = generate_csrf()
            # ...which also sets a value in `flask.session`, so we need to
            # ask Flask to save that value to the cookie jar in the test
            # client. This is where we actually use that request shim we made!
            flask.current_app.save_session(flask.session, request)
            # And finally, return that CSRF token we got from Flask-WTF.
            return csrf_token

    # Feel free to define other methods on this test client. You can even
    # use the `csrf_token` property we just defined, like we're doing here!
    def login(self, email, password):
        return self.post("/accounts/login", data={
            "email": email,
            "password": password,
            "csrf_token": self.csrf_token,
        }, follow_redirects=True)

    def logout(self):
        return self.get("/accounts/logout", follow_redirects=True)

# To hook up this extended test client class to your Flask application,
# assign it to the `test_client_class` property, like this:
# app = Flask(__name__)
# app.test_client_class = FlaskClient

# Now in your tests, you can request a test client the same way
# that you normally do:
# client = app.test_client()
# But now, `client` is an instance of the class we defined!

# In your tests, you can call the methods you defined, like this:
# client.login('user@example.com', 'passw0rd')

# And any time you need to pass a CSRF token, just use the `csrf_token`
# property, like this:
# client.post("/user/1", data={
#     "favorite_color": "blue",
#     "csrf_token": client.csrf_token,
# })
