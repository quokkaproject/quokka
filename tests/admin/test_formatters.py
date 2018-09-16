import pytest
import mock
from flask import current_app as app
from flask_htmlbuilder.htmlbuilder import html
from quokka.core.content.models import make_model
from quokka.admin.formatters import format_datetime, \
    format_view_on_site, format_ul, format_link, \
    format_status, format_url, format_custom_vars
from quokka.core.content.models import Content


################################
#pytest - fixtures - setUp();  #
################################
#fm = Formatters()


#####################################################
#pytest - Quokka - quokka/admin/test_formatters.py  #
#####################################################
#WIP:
#@mock.patch("quokka.core.content.models.Content")
#@mock.patch("quokka.core.content.models.make_model")
#def test_format_datetime(mock_make_model, mock_Content):
#    format_datetime(request='', obj=mock_Content, fieldname='')
#    assert mock_make_model.called is True

def test_format_view_on_site():
    pass

def test_format_ul():
    pass

def test_format_link():
    pass

def test_format_status():
    pass

def test_format_url():
    pass

def test_format_custom_vars():
    pass




