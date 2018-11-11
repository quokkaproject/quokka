import pytest
import mock
from werkzeug.routing import BaseConverter
from quokka.core.regex_url_support import RegexConverter, Regex
from quokka import create_app


#######################################################
#pytest - fixtures                                    #
#######################################################
app = create_app(test=True)
regex_converter = RegexConverter("quokka/mock/url", ("mock", list))
regex = Regex(app)

#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_class_RegexConverter_is_subclass():
    assert issubclass(RegexConverter, BaseConverter) == True

def test_class_RegexConverter_isinstance():
    assert isinstance(regex_converter, RegexConverter) == True

def test_class_RegexConverter_map_property():
    assert regex_converter.map == 'quokka/mock/url'

def test_class_RegexConverter_weight_property():
    assert regex_converter.weight == 100

def test_class_Regex_isinstance():
    assert isinstance(regex, Regex) == True

def test_class_Regex_name():
    assert regex.app.name == 'quokka'


