# coding: utf-8

from flask import request, session, redirect, current_app, url_for
from flask.ext.security.utils import login_user

from .models import User, Connection


def clean_sessions():
    for provider in current_app.config.get("OAUTH", {}):
        session.pop('%s_oauthredir' % provider, None)
        session.pop('oauth_%s_token' % provider, None)


def get_oauth_app(provider):
    provider_name = "oauth_" + provider
    return getattr(current_app, provider_name, None)


def oauth_login(provider):
    oauth_app = get_oauth_app(provider)
    clean_sessions()

    if provider == 'google':
        _next = None
    else:
        _next = request.args.get('next', request.referrer) or None

    return oauth_app.authorize(
        callback=url_for(
            '{0}_authorized'.format(provider),
            _external=True,
            next=_next
        )
    )


def make_oauth_handler(provider):

    def oauth_handler(resp):
        app = current_app
        oauth_app = get_oauth_app(provider)
        if not oauth_app:
            return "Access denied: oauth app not found"

        oauth_app.tokengetter(
            lambda: session.get("oauth_" + provider + "_token")
        )

        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session["oauth_" + provider + "_token"] = (resp['access_token'], '')
        data = app.config.get("OAUTH", {}).get(provider)
        me = oauth_app.get(data.get('_info_endpoint'))

        if not any([me.data.get('verified'),
                    me.data.get('verified_email')]):
            return "Access denied: email not verified"

        email = me.data.get('email')
        name = me.data.get('name')
        provider_user_id = me.data.get('id')
        profile_url = me.data.get('link')

        access_token = resp['access_token']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(
                name=name,
                email=email,
                username=User.generate_username(email)
            )
            user.save()

        try:
            connection = Connection.objects.get(
                user_id=str(user.id),
                provider_id=provider,
            )
            connection.access_token = access_token
            connection.save()
        except Connection.DoesNotExist:
            connection = Connection(
                user_id=str(user.id),
                provider_id=provider,
                provider_user_id=provider_user_id,
                profile_url=profile_url,
                access_token=access_token
            )
            connection.save()

        login_user(user)

        _next = request.args.get(
            'next', request.referrer
        ) or session.get(
            'next'
        ) or app.config.get('OAUTH_POST_LOGIN', "/")

        return redirect(_next)
    return oauth_handler
