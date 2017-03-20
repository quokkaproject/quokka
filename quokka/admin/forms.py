# coding: utf-8

from wtforms import fields as _fields
# from wtforms import form as _form
from flask_wtf import FlaskForm
from wtforms.meta import DefaultMeta
from flask_admin.babel import Translations
from quokka.admin.wtforms_html5 import AutoAttrMeta

fields = _fields  # noqa


class Form(FlaskForm):  # _form.Form):
    """Base class to customize wtforms"""
    _translations = Translations()
    Meta = AutoAttrMeta

    def _get_translations(self):
        return self._translations
