import pytest
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
from quokka.core.content.models import (
    Orderable, Series, Category, Fixed, Url, Author,
    Tag, Content, Article, Page, Block, BlockItem,
    make_model, make_paginator
)

################################################################################
#pytest - fixtures                                                             #
################################################################################
DEFAULT_DATE_FORMAT = '%a %d %B %Y'

class MockExtendsOrderableTestClass(Orderable):
    def debug_is_content(self):
        return self.is_content

series = Series("mock-name")
category = Category("mock-category")
fixed = Fixed(name="mock-name")
url = Url(name="mock-name")
author = Author(authors="mock-authors")
tag = Tag(name="mock-name")


#######################################################
#pytest - Quokka - tests/core/content/test_models.py  #
#######################################################
def test_orderable():
    meotc = MockExtendsOrderableTestClass()
    assert meotc.is_content == False

def test_seriesClass_all_property():
    assert series.all == []

def test_seriesClass_all_next():
    assert series.all_next == []

def test_seriesClass_all_prrevious():
    assert series.all_previous == []

def test_seriesClass_index():
    assert series.index == 1

def test_seriesClass_is_content():
    assert series.is_content == False

def test_seriesClass_name():
    assert series.name == 'mock-name'

def test_seriesClass_next():
    assert series.next == []

def test_seriesClass_previous():
    assert series.previous == []

def test_seriesClass_slug():
    assert series.slug == 'mock-name'
 
def test_series_class_property_external_url_atribute_error():
    with pytest.raises(AttributeError) as err:
        series.external_url(url="mock-url")
        assert "object has no attribute url" in str(err.value)
 
def test_category_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        category.external_url
        assert "Working outside of request context." in str(err.value)

def test_category_class_property_category():
    assert category.category == 'mock-category'

def test_category_class_property_is_content():
    assert category.is_content == False

def test_category_class_property_name():
    assert category.name == 'Mock Category'

def test_category_class_property_slug():
    assert category.slug == 'mock-category'

def test_category_class_property_url():
    assert category.url == 'mock-category'

def test_fixed_class_property_is_content():
    assert fixed.is_content == False

def test_fixed_class_property_name():
    assert fixed.name == 'mock-name'

def test_fixed_class_property_slug():
    assert fixed.slug == 'mock-name'

def test_fixed_class_property_url():    
    assert fixed.url == 'mock-name'

def test_fixed_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        fixed.external_url
        assert "Working outside of request context." in str(err.value)

def test_url_class_property_is_content():
    assert url.is_content == False

def test_url_class_property_name():
    assert url.name == 'mock-name'

def test_url_class_property_slug():
    assert url.slug == 'mock-name'

def test_url_class_property_url():    
    assert url.url == 'mock-name'

def test_url_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        url.external_url
        assert "Working outside of request context." in str(err.value)

def test_class_authors_property_authors():
    assert author.authors == 'mock-authors'

def test_class_authors_property_is_content():
    assert author.is_content == False

def test_class_authors_property_name():
    assert author.name == 'Mock Authors'

def test_class_authors_property_slug():
    assert author.slug == 'mock-authors'

def test_class_authors_property_social():
    assert author.social == {}

def test_class_authors_property_url():
    assert author.url == 'author/mock-authors'

def test_class_tag_property_is_content():
    assert tag.is_content == False

def test_class_tag_property_name():
    assert tag.name == 'mock-name'

def test_class_tag_property_slug():
    assert tag.slug == 'mock-name'

def test_class_tag_property_url():
    assert tag.url == 'tag/mock-name/index.html'

def test_content_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        content = Content(data="2018-11-01")
        assert "working outside of request context." in str(err.value)

def test_article_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        article = Article(data="2018-11-01")
        assert "working outside of request context." in str(err.value)

def test_page_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        page = Page(data="2018-11-01")
        assert "working outside of request context." in str(err.value)

def test_block_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        block = Block(data="2018-11-01")
        assert "working outside of request context." in str(err.value)

def test_blockitem_class_property_external_url_atribute_error():
    with pytest.raises(RuntimeError) as err:
        block = BlockItem(data="2018-11-01")
        assert "working outside of request context." in str(err.value)

