import pytest
import mock
from quokka.utils.dateformat import pretty_date

def pretty_date():
    pretty = pretty_date()
    assert pretty == 'just now'
