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


#######################################################
#pytest - Quokka - tests/core/content/test_models.py  #
#######################################################
def test_Orderable():
    meotc = MockExtendsOrderableTestClass()
    assert meotc.is_content == False

def test_SeriesClass_all_property():
    assert series.all == []

def test_SeriesClass_all_next():
    assert series.all_next == []

def test_SeriesClass_all_prrevious():
    assert series.all_previous == []

def test_SeriesClass_index():
    assert series.index == 1

def test_SeriesClass_is_content():
    assert series.is_content == False

def test_SeriesClass_name():
    assert series.name == 'mock-name'

def test_SeriesClass_next():
    assert series.next == []

def test_SeriesClass_previous():
    assert series.previous == []

def test_SeriesClass_slug():
    assert series.slug == 'mock-name'
 
def test_Series_class_property_external_url_atribute_error():

    with pytest.raises(AttributeError) as err:
        try:
            series.external_url(url="mock-url")
            assert "object has no attribute url" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise





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




