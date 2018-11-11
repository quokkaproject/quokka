import pytest
import mock
from datetime import datetime
from werkzeug._compat import implements_to_string, string_types
from werkzeug.wrappers import BaseResponse
from quokka.utils.atom import (
    escape, _make_text_block,
    AtomFeed, FeedEntry
)


################################
#pytest - fixtures - setUp();  #
################################
XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'
make = _make_text_block(name="name-param-mock", content="content-param-mock")


##################################
#pytest - Quokka - test_atom.py  #
##################################
def test_escape():
    assert escape("mock-pytest-param") == "mock-pytest-param"

def test_make_text_block():
    assert make == '<name-param-mock>content-param-mock</name-param-mock>\n'


def test_format_iso8601():
    pass

#@implements_to_string
def test_class_AtomFeed():
    pass

#@implements_to_string
def test_class_FeedEntry():
    pass



