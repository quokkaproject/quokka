import pytest
import mock
from dynaconf.utils.parse_conf import (
    parse_conf_data
)
from quokka.utils.custom_vars import (
    parse_data, 
    custom_var_dict
)

def test_parse_data():
    data = parse_data("java")
    assert data == 'java'

def test_custom_var_dict():
    with pytest.raises(TypeError) as err:
        custom_var_dict(cvarlist = ['java', 'clang', 'c++lang', 'lisp'])
        assert "string indices must be integers" in str(err.value)

