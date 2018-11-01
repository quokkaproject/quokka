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


################################################################################
#pytest - fixtures                                                             #
################################################################################
class TestClassPytestExtendsAdminContentView(AdminContentView):
    def mock_init_method(self):
        return super(AdminContentView, self)

class TestClassMockColl():
    name = "mock-name"

coll = TestClassMockColl()


#################################################################################
#pytest - Quokka - tests/core/content/test_admin.py                             #
#################################################################################
def test_AdminContentViewMakeInstance():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    assert isinstance(mock_class, TestClassPytestExtendsAdminContentView) == True

def test_AdminContentView_create_defaults():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert AdminContentView_mocked.__thisclass__.create_defaults == {}

def test_AdminContentView_base_query():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.base_query == {}


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














