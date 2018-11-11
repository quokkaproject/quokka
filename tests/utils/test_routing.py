import pytest
import mock
from quokka.utils.routing import expose

def test_expose():
    assert expose() != ""
    
