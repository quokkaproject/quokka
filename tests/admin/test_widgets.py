import pytest
import mock
import json
from flask import current_app
#from quokka.core.template import render_template
from wtforms.widgets import TextArea, TextInput
from quokka.admin.widgets import TextEditor, PrepopulatedText


def test_TextEditor_is_instance():
    te = TextEditor()
    assert isinstance(te, TextEditor) == True

def test_TextEditor_cols():
    te = TextEditor()
    assert te.cols == 20

def test_TextEditor_css_cls():
    te = TextEditor()
    assert te.css_cls == 'text_editor'

def test_TextEditor_editor():
    te = TextEditor()
    assert te.editor == 'texteditor'

def test_TextEditor_rows():
    te = TextEditor()
    assert te.rows == 20

def test_TextEditor_style_():
    te = TextEditor()
    assert te.style_ == 'margin: 0px; width: 725px; height: 360px;'


def test_PrepopulatedText_is_instance():
    pt = PrepopulatedText()
    assert isinstance(pt, PrepopulatedText) is True

def test_PrepopulatedText_input_type():
    pt = PrepopulatedText()
    assert pt.input_type == 'text'

def test_PrepopulatedText_master():
    pt = PrepopulatedText()
    assert pt.master == ''

def test_PrepopulatedText_def_html_params():
    pt = PrepopulatedText()
    assert pt.html_params() == ''

def test_PrepopulatedText_html_params_param_error_tag_name():
    with pytest.raises(TypeError) as err:
        try:
            pt = PrepopulatedText()
            pt.html_params("<div>")
            assert "html_params() takes 0 positional arguments but 1 was given" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise




def test_PrepopulatedText_html_params_param_error_tag():
    with pytest.raises(TypeError) as err:
        try:
            pt = PrepopulatedText()
            pt.html_params("textarea")
            assert "html_params() takes 0 positional arguments but 1 was given" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise















