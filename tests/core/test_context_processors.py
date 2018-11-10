import pytest
import mock
import click
from quokka.core.content.models import make_model, Category
from quokka.utils.blocks import build_menu, get_text_block, get_quokka_home
from quokka.core.context_processors import configure
from quokka import create_app


#######################################################
#pytest - fixtures                                    #
#######################################################
app = create_app(test=True)


#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_configure():
    assert configure(app) is None


