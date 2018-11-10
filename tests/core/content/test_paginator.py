import pytest
import mock
import click
import functools
import logging
import os
from collections import namedtuple
from math import ceil
from flask import current_app as app
import six
from quokka.core.content.paginator import (
    Paginator, Page
)


################################################################################
#pytest - fixtures                                                             #
################################################################################
logger = logging.getLogger(__name__)
PaginationRule = namedtuple(
    'PaginationRule',
    'min_page URL SAVE_AS',
)

DEFAULT_PP = [(1, '{name}/', '{name}/index{extension}'),
              (2, '{name}/{number}/', '{name}/{number}/index{extension}')]

class PaginatorClassMock():
    num_pages = None
    def __init__(self):
        self.num_pages=25

paginator_class_mock = PaginatorClassMock()
paginator = Page(
    name="name-mock", object_list=["list", "mock"], 
    number=12, paginator=paginator_class_mock, 
    settings="setttings-mock"
)


#################################################################################
#pytest - Quokka - test_paginator.py                                            #
#################################################################################
def test_class_Paginator():

    with pytest.raises(RuntimeError) as err:
        try:
            paginator = Paginator("pytest-mock")
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


def test_class_Page_isinstance():
    assert isinstance(paginator, Page) == True

def test_class_Page_extension_property():
    assert paginator.extension == ''

def test_class_Page_name_property():
    assert paginator.name == 'name-mock'

def test_class_Page_number_property():
    assert paginator.number == 12

def test_class_Page_nnum_pages_property():
    assert paginator.paginator.num_pages == 25





