import mock
import pytest
from flask import Markup
from dynaconf.contrib import FlaskDynaconf
from dynaconf.utils import DynaconfDict
from dynaconf.loaders import yaml_loader, env_loader, default_loader
from quokka import create_app
from quokka.core.flask_dynaconf import configure_dynaconf


#######################################################
#pytest - fixtures                                    #
#######################################################
app = create_app(test=True)


#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_configure_dynaconf():
    conf = configure_dynaconf(app)
    assert conf is None


