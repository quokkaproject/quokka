# -*- coding: utf-8 -*-

from flask import session, current_app
from quokka_themes import render_theme_template


def render_template(template, **context):
    theme = session.get('theme', current_app.config.get('DEFAULT_THEME'))
    return render_theme_template(theme, template, **context)
