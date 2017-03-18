# coding: utf-8

from wtforms import fields as _fields
from wtforms import form as _form


fields = _fields  # noqa


class Form(_form.Form):
    """Base class to customize wtforms"""
