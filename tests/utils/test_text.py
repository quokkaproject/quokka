import pytest
import mock
from flask import request
from urllib.parse import urljoin
from slugify.main import Slugify
from quokka.utils.text import (
    abbreviate, normalize_var,
    make_social_link, make_social_link,
    make_social_name, cdata,
    make_external_url, split_all_category_roots
)

################################
#pytest - fixtures - setUp();  #
################################
slugify = Slugify()
slugify.to_lower = True
slugify_category = Slugify()
slugify_category.to_lower = True
slugify_category.safe_chars = '/'
abbrev = abbreviate("pytest-mock")


##################################
#pytest - Quokka - test_text.py  #
##################################
def test_abbreviate():
    debugger = abbreviate("pytest-mock")
    assert abbrev == 'pytest-mock'

def test_normalize_var():
    pass


def test_make_social_link():
    pass



def test_make_social_name():
    pass


def test_data():
    pass


def test_make_external_url():
    pass


def test_split_all_category_roots():
    pass
    
