import pytest
import mock
import time
from datetime import datetime
from werkzeug._compat import (
    implements_to_string, string_types
)
from werkzeug.wrappers import BaseResponse
from quokka.utils.atom import (
    escape, _make_text_block,
    AtomFeed, FeedEntry, 
    format_iso8601
)


################################
#pytest - fixtures - setUp();  #
################################
XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'
make = _make_text_block(name="name-param-mock", content="content-param-mock")
param_mock = {"title_type":"", "text":"", "url":"", "feed_url":"", "id":"", "updated":"",
"author":"", "icon":"", "logo":"", "rights":"", "rights_type":"", "subtitle":"", "subtitle_type":"", "generator":"", "links":""}


##################################
#pytest - Quokka - test_atom.py  #
##################################
def test_escape():
    assert escape("mock-pytest-param") == "mock-pytest-param"

def test_make_text_block():
    assert make == '<name-param-mock>content-param-mock</name-param-mock>\n'


def test_format_iso8601():
    format=format_iso8601(time)
    assert format != ""


def test_class_AtomFeed():

    with pytest.raises(ValueError) as err:
        try:
            atom = AtomFeed(title="title-mock", entries="entries-mock", kwargs=param_mock)
            assert "id is required" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_class_FeedEntry():

    with pytest.raises(ValueError) as err:
        try:
            atom = FeedEntry(title="title-mock", entries="entries-mock", kwargs=param_mock)
            assert "id is required" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except Exception:
            raise




