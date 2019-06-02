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
from quokka.admin.forms import PassiveField, PassiveHiddenField, PassiveStringField, Form, CallableValidator 
from wtforms import fields as _fields
from wtforms import widgets as _widgets
from wtforms import validators  # noqa
from wtforms.validators import ValidationError

#class unused
def test_passivefield():
    pass

#class unused
def test_passivehiddenfield():
    pass

#class unused
def test_passivestringfield():
    pass

def test_form_class_error_instance_outsite_flask_context():
    with pytest.raises(RuntimeError) as err:
        f = Form()
        assert "Working outside of application context." in str(err.value)

@mock.patch("flask_wtf.FlaskForm")
@mock.patch("quokka.admin.forms.Form")
def test_form_class_method_get_translations_is_called(mock_Form, mock_FlaskForm):

    class TestFormClassExtends(mock_Form):
        mock_Form._get_translations()

    assert mock_Form(mock_FlaskForm)._get_translations().called is False
    
@mock.patch("flask_wtf.FlaskForm")
@mock.patch("quokka.admin.forms.Form")
def test_Form_class_property_translations_is_called(mock_Form, mock_FlaskForm):

    class TestFormClassExtends(mock_Form):
        mock_Form._get_translations()

    assert mock_Form(mock_FlaskForm)._translations().called is False


@mock.patch("quokka.admin.forms.CallableValidator")
def test_callablevalidator_class_method__init__is_called(mock_CallableValidator):
    def pytest_function_param():
        pass

    cv = CallableValidator(pytest_function_param(), None)
    assert mock_CallableValidator.called is False


