import pytest
import mock
from quokka.core.monitoring import configure
from quokka import create_app


#######################################################
#pytest - fixtures                                    #
#######################################################
app = create_app(test=True)


#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_configure():
    conf = configure(app)
    assert conf is None


