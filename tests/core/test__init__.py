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
ce = configure_extensions(app)

#################################################################################
#pytest - Quokka - test_core__init__.py                                         #
#################################################################################
def test_app_equals_ce_instance():
    assert app == ce

def test_ce_equals_app_instance():
    assert ce == app

def test_ce_admin():
    with pytest.raises(KeyError) as err:
        try:
            ce.admin
            assert "admin" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except RuntimeError:
            raise

        except Exception:
            raise


def test_ce_before_requests_funcs():
    assert ce.before_request_funcs == {}

def test_ce_blueprints():
    assert ce.blueprints == {}

def test_ce_db():
    with pytest.raises(KeyError) as err:
        try:
            ce.db
            assert "db" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise

        except RuntimeError:
            raise

        except Exception:
            raise



def test_ce_debug():
    assert ce.debug == False

def test_ce_default_config():
    assert ce.default_config['TEMPLATES_AUTO_RELOAD'] == None
    assert ce.default_config['JSONIFY_MIMETYPE'] == 'application/json'
    assert ce.default_config['PROPAGATE_EXCEPTIONS'] == None
    assert ce.default_config['TESTING'] == False
    assert ce.default_config['DEBUG'] == None
    assert ce.default_config['ENV'] == None
    assert ce.default_config['MAX_COOKIE_SIZE'] == 4093

def test_ce_env():
    assert ce.env == "production"

def test_ce_error_handler_spec():
    assert ce.error_handler_spec == {}

def test_ce_extensions():
    assert ce.extensions == {}

def test_ce_got_first_request():
    assert ce.got_first_request == False

def test_ce_has_static_folder():
    assert ce.has_static_folder == True

def test_ce_import_name():
    assert ce.import_name == "quokka"

def test_ce_jinja_properties_env():
    assert ce.jinja_env.auto_reload == False
    assert ce.jinja_env.block_end_string == "%}"
    assert ce.jinja_env.block_start_string == "{%"
    assert ce.jinja_env.bytecode_cache == None
    assert ce.jinja_env.comment_end_string == "#}"
    assert ce.jinja_env.comment_start_string == "{#"
    assert ce.jinja_env.enable_async == False
    assert ce.jinja_env.exception_formatter == None
    assert ce.jinja_env.exception_handler == None

def test_ce_jinja_env_extensions():    
    assert ce.jinja_env.extensions['jinja2.ext.AutoEscapeExtension'] != ""
    assert ce.jinja_env.extensions['jinja2.ext.WithExtension'] != ""

def test_ce_jinja_env_filters_not_empty():    
    assert ce.jinja_env.filters['abs'] != ""
    assert ce.jinja_env.filters['attr'] != ""    
    assert ce.jinja_env.filters['batch'] != ""    
    assert ce.jinja_env.filters['capitalize'] != ""    
    assert ce.jinja_env.filters['center'] != ""    
    assert ce.jinja_env.filters['count'] != ""    
    assert ce.jinja_env.filters['d'] != ""    
    assert ce.jinja_env.filters['default'] != ""    
    assert ce.jinja_env.filters['dictsort'] != ""    
    assert ce.jinja_env.filters['e'] != ""    
    assert ce.jinja_env.filters['escape'] != ""    
    assert ce.jinja_env.filters['filesizeformat'] != ""    
    assert ce.jinja_env.filters['first'] != ""    
    assert ce.jinja_env.filters['float'] != ""    
    assert ce.jinja_env.filters['forceescape'] != ""    
    assert ce.jinja_env.filters['format'] != ""    
    assert ce.jinja_env.filters['groupby'] != ""    
    assert ce.jinja_env.filters['indent'] != ""    
    assert ce.jinja_env.filters['int'] != ""    
    assert ce.jinja_env.filters['lower'] != ""    
    assert ce.jinja_env.filters['map'] != ""    
    assert ce.jinja_env.filters['min'] != ""    
    assert ce.jinja_env.filters['max'] != ""    
    assert ce.jinja_env.filters['pprint'] != ""    
    assert ce.jinja_env.filters['random'] != ""    
    assert ce.jinja_env.filters['reject'] != ""    
    assert ce.jinja_env.filters['rejectattr'] != ""    
    assert ce.jinja_env.filters['replace'] != ""    
    assert ce.jinja_env.filters['reverse'] != ""    
    assert ce.jinja_env.filters['round'] != ""    
    assert ce.jinja_env.filters['safe'] != ""    
    assert ce.jinja_env.filters['select'] != ""    
    assert ce.jinja_env.filters['selectattr'] != ""    
    assert ce.jinja_env.filters['slice'] != ""    
    assert ce.jinja_env.filters['sort'] != ""    
    assert ce.jinja_env.filters['string'] != ""    
    assert ce.jinja_env.filters['striptags'] != ""    
    assert ce.jinja_env.filters['sum'] != ""    
    assert ce.jinja_env.filters['title'] != ""    
    assert ce.jinja_env.filters['trim'] != ""    
    assert ce.jinja_env.filters['abs'] != ""
    assert ce.jinja_env.filters['wordwrap'] != ""    

def test_ce_jinja_loader():
    assert ce.jinja_loader.encoding == 'utf-8'
    assert ce.jinja_loader.followlinks == False
    assert ce.jinja_loader.has_source_access == True
    assert ce.jinja_loader.searchpath != ""

def test_ce_jinja_options():
    assert ce.jinja_options['extensions'][0] == 'jinja2.ext.autoescape'
    assert ce.jinja_options['extensions'][1] == 'jinja2.ext.with_'

def test_ce_logger():
    assert ce.logger.disabled == False
    assert ce.logger.level == 0
    assert ce.logger.manager.disable == 0
    assert ce.logger.manager.emittedNoHandlerWarning == False
    assert ce.logger.manager.loggerClass == None
    assert ce.logger.manager.root.name == 'root'    
   
def test_ce_name():
    assert ce.name == "quokka"

def test_ce_permanent_session_lifetime():
    assert ce.permanent_session_lifetime.days == 31
    assert ce.permanent_session_lifetime.max.days == 999999999
    assert ce.permanent_session_lifetime.microseconds == 0
    assert ce.permanent_session_lifetime.min.days == -999999999
    assert ce.permanent_session_lifetime.seconds == 0

def test_ce_preserve_context_on_exception():
    assert ce.preserve_context_on_exception == False

def test_ce_propagate_exceptions():
    assert ce.propagate_exceptions == True

def test_ce_root_path():
    assert ce.root_path != ""

def test_ce_secret_key():
    assert ce.secret_key == None

def test_ce_send_file_max_age_default():
    assert ce.send_file_max_age_default.days == 0
    assert ce.send_file_max_age_default.microseconds == 0
    assert ce.send_file_max_age_default.seconds == 43200

def test_ce_session_cookie_name():
    assert ce.session_cookie_name == "session"

def test_ce_session_interface():
    assert ce.session_interface.key_derivation == "hmac"
    assert ce.session_interface.pickle_based == False
    assert ce.session_interface.salt == "cookie-session"

def test_ce_shell_context_processors():
    assert ce.shell_context_processors == []

def test_ce_static_folder():
    assert ce.static_folder != ""

def test_ce_static_url_path():
    assert ce.static_url_path == "/static"

def test_ce_subdomain_matching():
    assert ce.subdomain_matching == False

def test_ce_teardown_appcontext_funcs():
    assert ce.teardown_appcontext_funcs == []

def test_ce_teardown_request_funcs():
    assert ce.teardown_request_funcs == {}

def test_ce_template_folder():
    assert ce.template_folder == "templates"

def test_ce_templates_auto_reload():
    assert ce.templates_auto_reload == False

def test_ce_test_cli_runner_class():
    assert ce.test_cli_runner_class == None

def test_ce_test_client_class():
    assert ce.test_client_class == None

def test_ce_testing():
    assert ce.testing == True

def test_ce_theme_context():
    assert ce.theme_context['DEFAULT_LANG'] == None
    assert ce.theme_context['PAGES'] == []
    assert ce.theme_context['tags'] == []
    assert ce.theme_context['articles'] == []
    assert ce.theme_context['categories'] == []
    assert ce.theme_context['tag_cloud'] == []
    assert ce.theme_context['USE_LESS'] == False

def test_ce_url_build_error_handlers():
    assert ce.url_build_error_handlers == []

def test_ce_url_default_functions():
    assert ce.url_default_functions == {}

def test_ce_url_map():
    assert ce.url_map.charset == 'utf-8'
    assert ce.url_map.default_subdomain == ''
    assert ce.url_map.encoding_errors == 'replace'
    assert ce.url_map.host_matching == False
    assert ce.url_map.redirect_defaults == True
    assert ce.url_map.sort_key == None
    assert ce.url_map.sort_parameters == False
    assert ce.url_map.strict_slashes == True

def test_ce_use_x_sendfile():
    assert ce.use_x_sendfile == False


