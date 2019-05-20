import time
import pytest
import mock
import click
import datetime

from quokka.utils.text import (
    slugify_category, slugify
)
from flask import current_app as app
from quokka.core.content.utils import (
    url_for_content,
    url_for_category,
    strftime
)

#######################################################
#pytest - fixtures                                    #
#######################################################
param_dict = {"java":"debugger", "slug":"slug-mock", "title":"title-mock"}

def get_year_format():
    date_timestamp = datetime.datetime.now()
    return date_timestamp.year.__str__()


#######################################################
#pytest - Quokka - tests/core/content/test_utils.py   #
#######################################################
def test_url_for_content():
    with pytest.raises(RuntimeError) as err:
        url = url_for_content(content=param_dict)
        assert "Working outside of application context." in str(err.value)

def test_url_for_category():
    url = url_for_category("java-categoty-mock")
    assert url == "java-categoty-mock"

def test_strftime():
    assert strftime(time, "%Y") == get_year_format()

