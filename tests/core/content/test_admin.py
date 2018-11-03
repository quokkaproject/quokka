import warnings
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

class TestAdminArticlesView(AdminArticlesView):
    def init_super_method(self):
        return super(AdminArticlesView, self)

class TestAdminPagesView(AdminPagesView):
    def init_super_method(self):
        return super(AdminPagesView, self)
                          
class TestAdminBlocksView(AdminBlocksView):
    def init_super_method(self):
        return super(AdminBlocksView, self)

class TestClassMockColl():
    name = "mock-name"

coll = TestClassMockColl()

mock_column_list = (
    'title',
    'category',
    'authors',
    'date',
    'modified',
    'language',
    'published',
    'view'
)

mock_column_sortable_list = (
    'title',
    'category',
    'authors',
    'date',
    'modified',
    'language',
    'published'
)

mock_column_default_sort = ('date', True)

mock_column_details_list = [
    'title',
    'category',
    'slug',
    'content_format',
    'content_type',
    'language',
    'date',
    'created_by',
    'modified',
    'modified_by',
    'version',
    '_isclone',
    'quokka_module',
    'quokka_format_module',
    'quokka_format_class',
    'quokka_create_form_module',
    'quokka_create_form_class',
    'category_slug',
    'authors_slug',
    'authors_string',
    'tags_slug',
    'tags_string',
    'custom_vars',
]


mock_base_query = {'content_type': 'page'}

mock_create_defaults = {'comments': False}

mock_quokka_form_create_rules = [
    rules.FieldSet(('title', 'summary')),
    rules.FieldSet(('content_format',)),
    rules.csrf_token
]
    
mock_quokka_form_edit_rules = [
    rules.FieldSet(('title', 'summary')),
    rules.Field('content'),
    # rules.FieldSet(('category', 'authors', 'tags')),
    rules.FieldSet(('date',)),
    rules.FieldSet(('slug',)),
    rules.Field('published'),
    rules.Field('comments'),
    rules.Field('custom_vars'),
    rules.csrf_token
]

mock_base_query_article = {'content_type': 'article'}

mock_create_defauts_article = {'comments': True}

mock_base_query_admin_block = {'content_type': 'block'}

mock_create_defaults_admin_block = {'comments': False}

mock_column_list_admin_block = (
    'title',
    'date',
    'modified',
    'language',
    'published'
)

mock_column_sortable_list_admin_block = (
    'title',
    'date',
    'modified',
    'language',
    'published'
)

mock_quokka_form_create_rules_admin_block = [
    rules.FieldSet(('title', 'summary')),
    rules.FieldSet(('content_format',)),
    rules.csrf_token
]

mock_quokka_form_edit_rules_admin_block = [
    rules.FieldSet(('title', 'summary')),
    rules.Field('content'),
    # rules.FieldSet(('category', 'authors', 'tags')),
    rules.FieldSet(('date',)),
    rules.FieldSet(('slug',)),
    rules.Field('published'),
    rules.Field('comments'),
    rules.Field('block_items'),
    rules.Field('custom_vars'),
    rules.csrf_token
]





#################################################################################
#pytest - Quokka - tests/core/content/test_admin.py                             #
#################################################################################
def test_warnings_TestClassPytestExtendsAdminContentView():
    with pytest.warns(RuntimeWarning):
        class TestClassPytestExtendsAdminContentView(AdminContentView):
            def mock_init_method(self):
                return super(AdminContentView, self)
        warnings.warn("cannot collect test class", RuntimeWarning)

def test_warnings_TestAdminArticlesView():
    with pytest.warns(RuntimeWarning):
        class TestAdminArticlesView(AdminArticlesView):
            def init_super_method(self):
                return super(AdminArticlesView, self)
        warnings.warn("cannot collect test class", RuntimeWarning)

def test_warnings_TestAdminPagesView():
    with pytest.warns(RuntimeWarning):
        class TestAdminPagesView(AdminPagesView):
            def init_super_method(self):
                return super(AdminPagesView, self)
        warnings.warn("cannot collect test class", RuntimeWarning)

def test_warnings_TestAdminBlocksView():
    with pytest.warns(RuntimeWarning):
        class TestAdminBlocksView(AdminBlocksView):
            def init_super_method(self):
                return super(AdminBlocksView, self)
        warnings.warn("cannot collect test class", RuntimeWarning)

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

def test_AdminContentView_quokka_form_edit_rules():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.quokka_form_edit_rules == None

def test_AdminContentView_quokka_form_create_rules():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.quokka_form_create_rules == None

def test_AdminContentView_quokka_details_modal():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.details_modal == True

def test_AdminContentView_quokka_can_view_details():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.can_view_details == True

def test_AdminContentView_quokka_create_template():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.create_template == 'admin/quokka/create.html'
    
def test_AdminContentView_quokka_edit_template():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.edit_template == 'admin/quokka/edit.html'

def test_AdminContentView_quokka_page_size():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.page_size == 20

def test_AdminContentView_quokka_can_set_page_size():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.can_set_page_size == True

def test_AdminContentView_quokka_column_list():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.column_list == mock_column_list

def test_AdminContentView_quokka_column_sortable_list():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.column_sortable_list == mock_column_sortable_list

def test_AdminContentView_quokka_column_default_sort():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.column_default_sort == mock_column_default_sort

def test_AdminContentView_quokka_column_details_list():
    mock_class = TestClassPytestExtendsAdminContentView(coll)
    AdminContentView_mocked = mock_class.mock_init_method()
    assert  AdminContentView_mocked.__thisclass__.column_details_list == mock_column_details_list

def test_AdminArticlesView_base_query():
    mock_class = TestAdminArticlesView(coll)
    assert mock_class.base_query == mock_base_query_article

def test_AdminArticlesView_create_defaults():
    mock_class = TestAdminArticlesView(coll)
    assert mock_class.create_defaults == mock_create_defauts_article

def test_AdminPagesView_mock_base_query():
    mock_class = TestAdminPagesView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.base_query == mock_base_query

def test_AdminPagesView_mock_create_defaults():
    mock_class = TestAdminPagesView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.create_defaults == mock_create_defaults
    
def test_AdminPagesView_mock_quokka_form_create_rules():
    mock_class = TestAdminPagesView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.quokka_form_create_rules != mock_quokka_form_create_rules

def test_AdminPagesView_mock_quokka_form_mock_quokka_form_edit_rules():
    mock_class = TestAdminPagesView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.quokka_form_edit_rules != mock_quokka_form_edit_rules

def test_AdminBlocksView_mock_quokka_mock_base_query_admin_block():
    mock_class = TestAdminBlocksView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.base_query == mock_base_query_admin_block

def test_AdminBlocksView_mock_quokka_mock_create_defaults_admin_block():
    mock_class = TestAdminBlocksView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.create_defaults == mock_create_defaults_admin_block

def test_AdminBlocksView_mock_quokka_mock_column_list_admin_block():
    mock_class = TestAdminBlocksView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.column_list == mock_column_list_admin_block

def test_AdminBlocksView_mock_quokka_mock_column_sortable_list_admin_block():
    mock_class = TestAdminBlocksView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.column_sortable_list == mock_column_sortable_list_admin_block

def test_AdminBlocksView_mock_quokka_mock_quokka_form_create_rules_admin_block():
    mock_class = TestAdminBlocksView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.quokka_form_create_rules != mock_quokka_form_create_rules_admin_block

def test_AdminBlocksView_mock_quokka_mock_quokka_form_edit_rules_admin_block():
    mock_class = TestAdminBlocksView(coll)
    AdminPagesView_mocked = mock_class.init_super_method()
    assert AdminPagesView_mocked.__thisclass__.quokka_form_edit_rules != mock_quokka_form_edit_rules_admin_block









