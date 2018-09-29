import mock
import click
import functools
from quokka.core.content.utils import url_for_content
from quokka.core.content.formats import get_format
from quokka.core.content.paginator import Paginator
from flask import url_for
from flask import current_app as app
from quokka.utils.text import (
    slugify, slugify_category, make_social_link,
    make_social_name, make_external_url
)
from quokka.utils.dateformat import pretty_date
from quokka.utils.custom_vars import custom_var_dict


DEFAULT_DATE_FORMAT = '%a %d %B %Y'


#@functools.total_ordering
def test_Orderable():
    pass


def test_Series():
    pass

def test_Category():
    pass

def test_Fixed():
    pass

def test_Url():
    pass

def test_Author():
    pass

def test_Tag():
    pass

def test_Content():
    pass


def test_class_Article():
    pass
    

def test_class_Page():
    pass


def test_class_Block():
    pass


def test_class_BlockItem():
    pass

def test_make_model():
    pass


def test_make_paginator():
    pass




