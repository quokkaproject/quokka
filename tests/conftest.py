import os
import pytest
from quokka import create_app

################################
#pytest - fixtures - setUp();  #
################################
@pytest.fixture
def app():
   """Flask Pytest uses it"""
   os.chdir('quokka/project_template/')
   return create_app()
