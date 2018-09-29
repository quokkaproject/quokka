import pytest
import mock
from flask import request
from urllib.parse import urljoin
from slugify.main import Slugify


################################
#pytest - fixtures - setUp();  #
################################
slugify = Slugify()
slugify.to_lower = True
slugify_category = Slugify()
slugify_category.to_lower = True
slugify_category.safe_chars = '/'



##################################
#pytest - Quokka - test_text.py  #
##################################
def test_abbreviate():
    pass


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
    
