# -*- coding: utf-8 -*-
import logging
from speaklater import make_lazy_string
from quokka.modules.accounts.models import User

logger = logging.getLogger()


def lazy_str_setting(key, default=None):
    from flask import current_app
    return make_lazy_string(
        lambda: current_app.config.get(key, default)
    )


def get_current_user():
    from flask.ext.security import current_user
    try:
        return User.objects.get(id=current_user.id)
    except Exception as e:
        logger.warning("No user found: {}".format(e))
        return current_user


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
