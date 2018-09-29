import mock
import pytest
import datetime as dt
import getpass
import json
from quokka.core.content.parsers import markdown
from flask import current_app as app, Markup
from flask_admin.helpers import get_form_data
from flask_admin.model.fields import InlineFieldList, InlineFormField
from quokka.admin.forms import Form, fields, rules, validators
from werkzeug.utils import import_string
from quokka.core.content.formats import get_content_formats, get_content_format_choices, get_format,get_edit_form,validate_category, get_category_kw, validate_block_item,get_block_item_kw, get_default_category, get_authors_kw, get_default_author,get_tags_kw,get_default_language,BaseForm,CreateForm,CustomVariablesForm,BlockItemForm,BaseEditForm,BaseFormat,PlainEditForm,PlainFormat,HTMLEditForm,HTMLFormat,MarkdownFormat, MarkdownEditForm


def test_get_content_formats():
    pass


def test_get_content_format_choices():
    pass


def test_get_format():
    pass

def test_get_edit_form():
    pass

def test_validate_category():
    pass

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


