import pytest
import mock
from flask_admin.babel import Translations
from flask_admin.form import rules  # noqa
from flask_admin.form.fields import (DateTimeField, JSONField, Select2Field,
                                     Select2TagsField, TimeField)
from flask_admin.form.widgets import Select2TagsWidget
from flask_admin.model.fields import InlineFieldList, InlineFormField
from flask_wtf import FlaskForm
from quokka.admin.fields import SmartSelect2Field
from quokka.admin.wtforms_html5 import AutoAttrMeta
from wtforms import fields as _fields
from wtforms import widgets as _widgets
from wtforms import validators  # noqa
from wtforms.validators import ValidationError

#class unused
def test_PassiveField():
    pass

#class unused
def test_PassiveHiddenField():
    pass

#class unused
def test_PassiveStringField():
    pass

def test_Form():
    pass

def test_CallableValidator():
    pass


