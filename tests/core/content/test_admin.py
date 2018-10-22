import mock
import pytest
import datetime as dt
import pymongo
from flask import current_app
from quokka.admin.forms import ValidationError, rules
from quokka.admin.views import ModelView, RequiresLogin
#from quokka.admin.formatters import (
#    format_datetime, format_view_on_site, format_custom_vars
#)
from quokka.core.auth import get_current_user
from quokka.utils.text import slugify, slugify_category
from quokka.core.content.formats import CreateForm, get_format
from quokka.core.content.utils import url_for_content
from quokka.core.content.admin import AdminContentView, AdminArticlesView, AdminPagesView, AdminBlocksView
from flask_admin.contrib.pymongo import ModelView
from quokka.admin.actions import CloneAction, PublishAction


"""
['assert_any_call', 'assert_called', 'assert_called_once', 'assert_called_once_with', 'assert_called_with', 'assert_has_calls', 'assert_not_called', 'attach_mock', 'call_args', 'call_args_list', 'call_count', 'called', 'configure_mock', 'method_calls', 'mock_add_spec', 'mock_calls', 'reset_mock', 'return_value', 'side_effect']
"""

#@mock.patch("quokka.core.content.admin.AdminContentView")
#@mock.patch("flask_admin.contrib.pymongo.ModelView")
#@mock.patch("quokka.admin.views.RequiresLogin")
#@mock.patch("quokka.admin.actions.PublishAction")
#@mock.patch("quokka.admin.actions.CloneAction")
#def test_AdminContentView(mock_CloneAction, mock_PublishAction, mock_RequiresLogin, mock_ModelView, mock_AdminContentView):
#    #mock_actions = ['mock_attr1', 'mock_attr2', 'mock_attr3']
#
#    mock_mv = mock_ModelView(mock_CloneAction, mock_PublishAction, mock_RequiresLogin, mock_ModelView)
#    print(dir(mock_CloneAction))
#    #mock_mv._action = ['mock_attr1', 'mock_attr2', 'mock_attr3']
#    #mock_acv =  mock_AdminContentView(mock_mv)
#    #acv.create_form()
#    #print("debugger-pytest=>"+acv)
#    #print(dir(mock_acv.create_form()))
#    #assert mock_acv.create_form.assert_any_call is True
#    #assert isinstance(mock_mv, mock_ModelView) == True
#    assert mock_mv.assert_not_called is True

def test_AdminContentView():
    pass 

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


