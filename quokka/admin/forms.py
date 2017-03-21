# coding: utf-8

from wtforms import fields as _fields
from flask_wtf import FlaskForm
from flask_admin.babel import Translations
from quokka.admin.wtforms_html5 import AutoAttrMeta
from quokka.admin.fields import SmartSelect2Field
from flask_admin.form.fields import (
    DateTimeField,
    TimeField,
    Select2Field,
    Select2TagsField,
    JSONField
)
from flask_admin.model.fields import (
    InlineFieldList,
    InlineFormField
)
from flask_admin.form import rules  # noqa

fields = _fields  # noqa
fields.SmartSelect2Field = SmartSelect2Field
fields.DateTimeField = DateTimeField
fields.TimeField = TimeField
fields.Select2Field = Select2Field
fields.Select2TagsField = Select2TagsField
fields.JSONField = JSONField
fields.InlineFieldList = InlineFieldList
fields.InlineFormField = InlineFormField


class Form(FlaskForm):
    """Base class to customize wtforms"""
    _translations = Translations()
    Meta = AutoAttrMeta

    def _get_translations(self):
        return self._translations
