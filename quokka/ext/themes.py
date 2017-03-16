# coding: utf-8

from quokka_themes import Themes


def configure(app):
    themes = Themes()
    themes.init_themes(app, app_identifier="quokka")
