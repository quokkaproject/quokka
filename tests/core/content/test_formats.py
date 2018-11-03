import mock
import pytest
import datetime as dt
import getpass
import json
from flask_admin import Admin
from quokka.core.content.parsers import markdown
from flask import current_app as app, Markup
from flask_admin.helpers import get_form_data
from flask_admin.model.fields import InlineFieldList, InlineFormField
from quokka.admin.forms import Form, fields, rules, validators
from werkzeug.utils import import_string
from quokka.core.content.formats import (
        get_content_formats, get_content_format_choices, get_format, 
        get_edit_form, validate_category, get_category_kw, 
        validate_block_item, get_block_item_kw, get_default_category, 
        get_authors_kw, get_default_author, get_tags_kw, get_default_language,
        BaseForm, CreateForm, CustomVariablesForm, BlockItemForm,
        BaseEditForm, BaseFormat, PlainEditForm, PlainFormat,
        HTMLEditForm, HTMLFormat, MarkdownFormat, MarkdownEditForm
)

################################################################################
#pytest - !!!module warning!!!                                                 # 
#the module quokka.core.content.formats                                        #
#contains def and class not used by this project, nobody call this module      #
################################################################################


################################################################################
#pytest - fixtures                                                             #
################################################################################
mock_obj = {'content_format' : 'debugger'}

class MockFields():
    data = "mock,url,to,pytest"

mock_fields = MockFields()



#################################################################################
#pytest - Quokka - tests/core/content/test_formats_.py                          #
#################################################################################
def test_get_content_formats_def_instance_error_outside_context():
    
    with pytest.raises(RuntimeError) as err:
        try:
            get_content_formats()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise



def test_get_content_format_choices_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_content_format_choices()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_get_format_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_format(mock_obj)
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_get_edit_form_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_edit_form(mock_obj)
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_validate_category_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            validate_category(None, fields)
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_get_category_kw_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_category_kw(fields)
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_validate_block_item_def_should_retur_error_message_notice():
    assert validate_block_item(None, mock_fields) == "You can select only one URL for each item"


def test_get_block_item_kw_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_block_item_kw(fields)
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_get_default_category_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_default_category()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_get_authors_kw_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_authors_kw(fields)
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_get_default_author_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_default_author()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_get_tags_kw_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_tags_kw(fields)
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_get_default_language_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            get_default_language()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_BaseForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            trying_make_a_instance = BaseForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_CreateForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            trying_make_a_instance = CreateForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_CustomVariablesForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            trying_make_a_instance = CustomVariablesForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise



def test_BlockItemForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            trying_make_a_instance = BlockItemForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_BaseEditForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            trying_make_a_instance = BaseEditForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_BaseFormat_class_instance_error_outside_context():
    with pytest.raises(TypeError) as err:
        try:
            trying_make_a_instance = BaseFormat(BaseForm)
            assert "takes no parameters" in str(err.value)

        except AttributeError as atterr:
            assert "object has no attribute" in str(atterr.value)

        except RuntimeError as e:
            raise

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_PlainEditForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        
        
        try:
            trying_make_a_instance = PlainEditForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_PlainFormat_class_instance_is_same_PlanEditForm():
    pf = PlainFormat()
    assert (type(pf.edit_form) == type(PlainEditForm)) is True

def test_HTMLEditForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            trying_make_a_instance = HTMLEditForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise

def test_HTMLFormat_class_isinstance_of_HTMLFormat():
    html = HTMLFormat()
    assert isinstance(html, HTMLFormat) is True


def test_MarkdownEditForm_class_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            trying_make_a_instance = MarkdownEditForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
        except FileExistsError:
            raise

        except Exception:
            raise


def test_MarkdownFormat_class_isinstance_of_MarkdownFormat():
    mf = MarkdownFormat()
    assert isinstance(mf, MarkdownFormat) is True




