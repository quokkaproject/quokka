# coding utf-8

from flask import session
from flask.ext.oauthlib.client import OAuth

from quokka.modules.accounts.oauth import make_oauth_handler, oauth_login


def configure(app):
    """
    will build oauthlib remote apps from config vairable in form of

    OAUTH = {
        "google": {
            "consumer_key": 'xxxxxxxxxxxx',
            "consumer_secret": 'xxxxxxxxxxxxxxxxxxxx',
            "request_token_params": {
                'scope': ('https://www.googleapis.com/auth/userinfo.email '
                          'https://www.googleapis.com/auth/userinfo.profile')
            },
            "base_url": 'https://www.googleapis.com/oauth2/v1/',
            "request_token_url": None,
            "access_token_method": 'POST',
            "access_token_url": 'https://accounts.google.com/o/oauth2/token',
            "authorize_url": 'https://accounts.google.com/o/oauth2/auth',
            "_info_endpoint": "userinfo"
        },
        "facebook": {
            "consumer_key": "xxxxxxxxxxxxxxxxxxxxxxxx",
            "consumer_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
            "request_token_params": {'scope': 'email'},
            "base_url": 'https://graph.facebook.com',
            "request_token_url": None,
            "access_token_url": '/oauth/access_token',
            "authorize_url": 'https://www.facebook.com/dialog/oauth',
            "_info_endpoint": "/me"
        },
        "github": {},
        "linkedin": {},
        "dropbox": {},
        "twitter": {}
    }
    """

    app.add_url_rule(
        '/accounts/oauth/login/<provider>/',
        'oauth_login',
        oauth_login
    )

    config = app.config.get("OAUTH")
    if not config:
        return

    oauth = OAuth(app)

    for provider, data in config.items():
        provider_name = "oauth_" + provider
        oauth_app = oauth.remote_app(
            provider,
            **{k: v for k, v in data.items() if not k.startswith("_")}
        )

        token_var = "oauth_{}_token".format(provider)
        oauth_app.tokengetter(lambda: session.get(token_var))

        setattr(app, provider_name, oauth_app)

        app.add_url_rule(
            '/accounts/oauth/authorized/{0}/'.format(provider),
            '{0}_authorized'.format(provider),
            oauth_app.authorized_handler(make_oauth_handler(provider))
        )

        if provider == 'linkedin':
            def change_linkedin_query(uri, headers, body):
                auth = headers.pop('Authorization')
                headers['x-li-format'] = 'json'
                if auth:
                    auth = auth.replace('Bearer', '').strip()
                    if '?' in uri:
                        uri += '&oauth2_access_token=' + auth
                    else:
                        uri += '?oauth2_access_token=' + auth
                return uri, headers, body

            oauth_app.pre_request = change_linkedin_query
