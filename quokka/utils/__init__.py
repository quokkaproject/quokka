# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger()


def lazy_setting(key, default=None):
    from speaklater import make_lazy_string
    from flask import current_app
    return make_lazy_string(
        lambda: current_app.config.get(key, default)
    )


def lazy_str_setting(key, default=None):
    return str(lazy_setting(key, default))


def get_current_user():
    from quokka.modules.accounts.models import User
    from flask.ext.security import current_user
    try:
        return User.objects.get(id=current_user.id)
    except Exception as e:
        logger.warning("No user found: %s", str(e))
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


def parse_conf_data(data):
    """
    $int $bool $float $json (for lists and dicts)
    strings does not need converters

    export QUOKKA_DEFAULT_THEME='material'
    export QUOKKA_DEBUG='$bool True'
    export QUOKKA_DEBUG_TOOLBAR_ENABLED='$bool False'
    export QUOKKA_PAGINATION_PER_PAGE='$int 20'
    export QUOKKA_MONGODB_SETTINGS='$json {"DB": "quokka_db", "HOST": "mongo"}'
    export QUOKKA_ALLOWED_EXTENSIONS='$json ["jpg", "png"]'
    """
    import json
    true_values = ('t', 'true', 'enabled', '1', 'on')
    converters = {
        '$int': int,
        '$float': float,
        '$bool': lambda value: True if value.lower() in true_values else False,
        '$json': json.loads
    }
    if data.startswith(tuple(converters.keys())):
        parts = data.partition(' ')
        converter_key = parts[0]
        value = parts[-1]
        return converters.get(converter_key)(value)
    return data
