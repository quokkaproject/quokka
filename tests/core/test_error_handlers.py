import mock
import click
from flask import render_template
from quokka import create_app
from quokka.core.error_handlers import configure

#######################################################
#pytest - fixtures                                    #
#######################################################
app = create_app(test=True)


#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_configure():
    assert configure(app) is None



