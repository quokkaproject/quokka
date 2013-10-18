# -*- coding: utf-8 -*-

from flask import session, current_app
from quokka_themes import render_theme_template


def render_template(template, theme=None, **context):
    theme = theme or []
    if not isinstance(theme, (list, tuple)):
        theme = [theme]

    sys_theme = session.get('theme', current_app.config.get('DEFAULT_THEME'))
    if sys_theme:
        theme.append(sys_theme)

    return render_theme_template(theme, template, **context)
