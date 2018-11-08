import mock
import click
import functools
import logging
import os
from collections import namedtuple
from math import ceil
from flask import current_app as app
import six
from quokka.core.content.paginator import Paginator, Page


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


#################################################################################
#pytest - Quokka - test_paginator.py                                            #
#################################################################################
def test_class_Paginator():
    pass

def test_class_Page():
    pass



