import pytest
import mock
import logging
from quokka.core.logger import configure
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


