import mock                                                                                                                                                                    
import pytest                                                                                                                                                                  
from inspect import getargspec                                                                                                                                                 
import sys
import import_string
from quokka import create_app
from quokka.core.app import QuokkaModule
from quokka.core.content.admin import AdminArticlesView, AdminPagesView, AdminBlocksView
from quokka.core.content.views import (
    DetailView, PreviewView, ArticleListView, CategoryListView, TagListView,
    AuthorListView
)
from quokka.core.content.utils import url_for_content, strftime
from quokka.core.content import configure
from quokka import create_app
from quokka.core.content import configure
from quokka.core import configure_extension, configure_extensions


################################################################################
#pytest - fixtures                                                             #
################################################################################
app = create_app(test=True)       
#print(configure_extensions(app))
#<QuokkaApp 'quokka'>
ce = configure_extensions(app)

#################################################################################
#pytest - Quokka - test_core__init__.py                                         #
#################################################################################
def test_app_equals_ce_instance():
    assert app == ce

def test_ce_equals_app_instance():
    assert ce == app

#WIP:
"""
def test_ce_admin():
    assert ce.admin == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""

def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == ""



ce.blueprints
ce.db
ce.debug
ce.default_config
ce.env
ce.error_handler_spec
ce.extensions
ce.got_first_request
ce.has_static_folder
ce.import_name
ce.instance_path
ce.jinja_env
ce.jinja_loader
ce.jinja_options
ce.logger
ce.name
ce.permanent_session_lifetime
ce.preserve_context_on_exception
ce.propagate_exceptions
ce.root_path
ce.secret_key
ce.send_file_max_age_default
ce.session_cookie_name
ce.session_interface
ce.shell_context_processors
ce.static_folder
ce.static_url_path
ce.subdomain_matching
ce.teardown_appcontext_funcs
ce.teardown_request_funcs
ce.template_context_processors
ce.template_folder
ce.templates_auto_reload
ce.test_cli_runner_class
ce.test_client_class
ce.testing
ce.theme_context
ce.url_build_error_handlers
ce.url_default_functions
ce.url_map
ce.use_x_sendfile
ce.view_functions

"""




