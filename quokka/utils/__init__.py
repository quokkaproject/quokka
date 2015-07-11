# -*- coding: utf-8 -*-
import logging
from speaklater import make_lazy_string

logger = logging.getLogger()


def lazy_str_setting(key, default=None):
    from flask import current_app
    return make_lazy_string(
        lambda: current_app.config.get(key, default)
    )


def get_current_user():
    from quokka.modules.accounts.models import User
    from flask.ext.security import current_user
    try:
        return User.objects.get(id=current_user.id)
    except Exception as e:
        logger.warning("No user found: {}".format(e))
        return current_user


def get_current_user_for_models():
    """
    Hackish but needed for running tests outside application context
    Because Flask test context is not well configured yet
    :return: User or None
    """
    user = get_current_user()
    try:
        if not user.is_authenticated():
            return None
        return user
    except:
        return None


def is_accessible(roles_accepted=None, user=None):
    user = user or get_current_user()
    if user.has_role('admin'):
        return True
    if roles_accepted:
        accessible = any(
            [user.has_role(role) for role in roles_accepted]
        )
        return accessible
    return True
