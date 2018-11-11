import pytest
import mock
from flask import request
from urllib.parse import urljoin
from slugify.main import Slugify
from quokka.utils.text import (
    abbreviate, normalize_var,
    make_social_link, make_social_link,
    make_social_name, cdata,
    make_external_url, split_all_category_roots
)

################################
#pytest - fixtures - setUp();  #
################################
slugify = Slugify()
slugify.to_lower = True
slugify_category = Slugify()
slugify_category.to_lower = True
slugify_category.safe_chars = '/'
abbrev = abbreviate("pytest-mock")
norma = normalize_var("http://yahoo.com")
make_link = make_social_link(network="twitter", txt="http://twitter.com/python")
make_name = make_social_name('http://twitter.com/python')
data = cdata("py-cdata")
split = split_all_category_roots(cat="categoria1/categoria2/categoria3")


##################################
#pytest - Quokka - test_text.py  #
##################################
def test_abbreviate():
    debugger = abbreviate("pytest-mock")
    assert abbrev == 'pytest-mock'

def test_normalize_var():
    assert norma == "http:__yahoo.com"


def test_make_social_link():
    assert make_link == 'http://twitter.com/python'


def test_make_social_name():
    assert make_name == 'python'

def test_cdata():
    assert data == '<![CDATA[\npy-cdata\n]]>'    

def test_make_external_url():

    with pytest.raises(RuntimeError) as err:
        try:
            make_external_url("http://it.yahoo.com")
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



def test_split_all_category_roots():
    assert split[0] == 'categoria1/categoria2/categoria3'
    assert split[1] == 'categoria1/categoria2'
    assert split[2] == 'categoria1'

