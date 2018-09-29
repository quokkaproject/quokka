import mock
import pytest
import datetime as dt
import pymongo
from flask import current_app
from quokka.admin.forms import ValidationError, rules
from quokka.admin.views import ModelView, RequiresLogin
from quokka.admin.formatters import (
    format_datetime, format_view_on_site, format_custom_vars
)
from quokka.core.auth import get_current_user
from quokka.utils.text import slugify, slugify_category
from quokka.core.content.formats import CreateForm, get_format
from quokka.core.content.utils import url_for_content
from quokka.core.content.admin import AdminContentView, AdminArticlesView, AdminPagesView, AdminBlocksView
from flask_admin.contrib.pymongo import ModelView
from quokka.admin.actions import CloneAction, PublishAction

"""
@mock.patch("quokka.core.content.admin.AdminContentView")
@mock.patch("flask_admin.contrib.pymongo.ModelView")
@mock.patch("quokka.admin.views.RequiresLogin")
@mock.patch("quokka.admin.actions.PublishAction")
@mock.patch("quokka.admin.actions.CloneAction")
def test_AdminContentView(mock_CloneAction, mock_PublishAction, mock_RequiresLogin, mock_ModelView, mock_AdminContentView):
    #mock_actions = ['mock_attr1', 'mock_attr2', 'mock_attr3']

    mock_mv = mock_ModelView(mock_CloneAction, mock_PublishAction, mock_RequiresLogin, mock_ModelView)
    #mock_mv._action = ['mock_attr1', 'mock_attr2', 'mock_attr3']
    acv =  mock_AdminContentView(mock_mv)
    acv.create_form()
    #print("debugger-pytest=>"+acv)
    #print(dir(acv))
    assert acv.create_form.mock_calls is False

(.venv) [marcosptf@localhost quokka]$ pytest tests/core/content/test_admin.py
=============================================================================== test session starts ===============================================================================
platform linux -- Python 3.6.1, pytest-3.6.4, py-1.5.4, pluggy-0.7.1
rootdir: /home/marcosptf/developer/quokka, inifile:
plugins: mock-1.10.0, flask-0.10.0, django-3.3.3, cov-2.5.1
collected 3 items                                                                                                                                                                 

tests/core/content/test_admin.py F..                                                                                                                                        [100%]

==================================================================================== FAILURES =====================================================================================
______________________________________________________________________________ test_AdminContentView ______________________________________________________________________________

mock_CloneAction = <MagicMock name='CloneAction' id='140166471221032'>, mock_PublishAction = <MagicMock name='PublishAction' id='140166471220304'>
mock_RequiresLogin = <MagicMock name='RequiresLogin' id='140166471220976'>, mock_ModelView = <MagicMock name='ModelView' id='140166470577792'>
mock_AdminContentView = <MagicMock name='AdminContentView' id='140166470598496'>

    @mock.patch("quokka.core.content.admin.AdminContentView")
    @mock.patch("flask_admin.contrib.pymongo.ModelView")
    @mock.patch("quokka.admin.views.RequiresLogin")
    @mock.patch("quokka.admin.actions.PublishAction")
    @mock.patch("quokka.admin.actions.CloneAction")
    def test_AdminContentView(mock_CloneAction, mock_PublishAction, mock_RequiresLogin, mock_ModelView, mock_AdminContentView):
        #mock_actions = ['mock_attr1', 'mock_attr2', 'mock_attr3']
    
        mock_mv = mock_ModelView(mock_CloneAction, mock_PublishAction, mock_RequiresLogin, mock_ModelView)
        #mock_mv._action = ['mock_attr1', 'mock_attr2', 'mock_attr3']
        acv =  mock_AdminContentView(mock_mv)
        acv.create_form()
        #print("debugger-pytest=>"+acv)
        #print(dir(acv))
>       assert acv.create_form.mock_calls is True
E       AssertionError: assert [call()] is True
E        +  where [call()] = <MagicMock name='AdminContentView().create_form' id='140166470648104'>.mock_calls
E        +    where <MagicMock name='AdminContentView().create_form' id='140166470648104'> = <MagicMock name='AdminContentView()' id='140166470631552'>.create_form

tests/core/content/test_admin.py:33: AssertionError
======================================================================= 1 failed, 2 passed in 0.88 seconds ========================================================================
(.venv) [marcosptf@localhost quokka]$ 



"""
#@mock.patch("flask_admin.contrib.pymongo.ModelView")
#@mock.patch("quokka.admin.views.RequiresLogin")
#@mock.patch("quokka.admin.actions.PublishAction")
#@mock.patch("quokka.admin.actions.CloneAction")
#def test_AdminArticlesView():
#    #aav = AdminArticlesView()
#    pass

def test_AdminPagesView():
    pass

def test_AdminBlocksView():
    pass


