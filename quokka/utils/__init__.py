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
        if not current_user.is_authenticated():
            return None
    except RuntimeError:
        # Flask-Testing will fail
        pass

    try:
        return User.objects.get(id=current_user.id)
    except Exception as e:
        logger.warning("No user found: %s" % e.message)
        return None
