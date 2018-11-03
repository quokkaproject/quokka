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


def test_get_edit_form_def_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        try:
            validate_category()
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


def test_get_category_kw():
    pass

def test_validate_block_item():
    pass

def get_block_item_kw():
    pass

def test_get_default_category():
    pass

def test_get_authors_kw():
    pass

def test_get_default_author():
    pass

def test_get_tags_kw():
    pass

def test_get_default_language():
    pass

def test_BaseForm():
    pass

def test_CreateForm():
    pass

def test_CustomVariablesForm():
    pass

def test_BlockItemForm():
    pass

def test_BaseEditForm():
    pass

def test_BaseFormat():
    pass

def test_PlainEditForm():
    pass


def test_PlainFormat():
    pass

def test_HTMLEditForm():
    pass

def test_HTMLFormat():
    pass

def test_MarkdownEditForm():
    pass

def test_MarkdownFormat():
    pass


