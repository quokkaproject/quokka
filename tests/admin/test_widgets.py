import pytest
import mock
import json
from flask import current_app
from wtforms.widgets import TextArea, TextInput
from quokka.admin.widgets import TextEditor, PrepopulatedText


def test_texteditor_is_instance():
    te = TextEditor()
    assert isinstance(te, TextEditor) == True

def test_texteditor_cols():
    te = TextEditor()
    assert te.cols == 20

def test_texteditor_css_cls():
    te = TextEditor()
    assert te.css_cls == 'text_editor'

def test_texteditor_editor():
    te = TextEditor()
    assert te.editor == 'texteditor'

def test_texteditor_rows():
    te = TextEditor()
    assert te.rows == 20

def test_texteditor_style_():
    te = TextEditor()
    assert te.style_ == 'margin: 0px; width: 725px; height: 360px;'


def test_prepopulatedtext_is_instance():
    pt = PrepopulatedText()
    assert isinstance(pt, PrepopulatedText) is True

def test_prepopulatedtext_input_type():
    pt = PrepopulatedText()
    assert pt.input_type == 'text'

def test_prepopulatedtext_master():
    pt = PrepopulatedText()
    assert pt.master == ''

def test_prepopulatedtext_def_html_params():
    pt = PrepopulatedText()
    assert pt.html_params() == ''

def test_prepopulatedtext_html_params_param_error_tag_name():
    with pytest.raises(TypeError) as err:
        pt = PrepopulatedText()
        pt.html_params("<div>")
        assert "html_params() takes 0 positional arguments but 1 was given" in str(err.value)

def test_prepopulatedtext_html_params_param_error_tag():
    with pytest.raises(TypeError) as err:
        pt = PrepopulatedText()
        pt.html_params("textarea")
        assert "html_params() takes 0 positional arguments but 1 was given" in str(err.value)

