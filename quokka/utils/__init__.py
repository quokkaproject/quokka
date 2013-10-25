# -*- coding: utf-8 -*-
from flask import current_app
from speaklater import make_lazy_string


def lazy_str_setting(key, default=None):
    return make_lazy_string(
        lambda: current_app.config.get(key, default)
    )
