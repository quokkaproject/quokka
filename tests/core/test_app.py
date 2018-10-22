import mock
import click
import pytest
import quokka
from flask_admin import Admin
from quokka.admin.views import FileAdmin, IndexView, ModelView
from quokka.admin import create_admin, QuokkaAdmin, configure_admin
from quokka.core.app import QuokkaApp
from quokka.core.flask_dynaconf import configure_dynaconf    
from flask import Blueprint, Flask
from flask.helpers import _endpoint_from_view_func
from quokka.core.app import QuokkaApp, QuokkaModule


################################################################################
#pytest - fixtures                                                             #
################################################################################
appQk = QuokkaApp('quokka')
configure_dynaconf(appQk)
module = QuokkaModule(__name__)


#################################################################################
#pytest - Quokka - tests/core/test_app.py                                       #
#################################################################################


def test_class_QuokkaModule():
    assert module.deferred_functions == []
    assert module.has_static_folder == False
    assert module.json_decoder == None
    assert module.json_encoder == None
    assert module.root_path != ""
    assert module.static_folder == None
    assert module.static_url_path == None
    assert module.subdomain == None
    assert module.template_folder == 'templates'
    assert module.url_prefix == None
    assert module.url_values_defaults == {}
    assert module.warn_on_modifications == False


def test_QuokkaApp_class_is_instance_of():
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    assert isinstance(qa, QuokkaAdmin) == True


def test_QuokkaApp_class_instance_register_method():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    assert qa.name == "Admin"


def test_QuokkaApp_class_instance_add_icon_method_assert_endpoint():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    
    qa.add_icon("http://endpoint.pytest", "icon.png", "text.pytest")
    assert 'http://endpoint.pytest' in appQk.config.get('ADMIN_ICONS')[0]


def test_QuokkaApp_class_instance_add_icon_method_assert_icon():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    
    qa.add_icon("http://endpoint.pytest", "icon.png", "text.pytest")
    assert 'icon.png' in appQk.config.get('ADMIN_ICONS')[0]


def test_QuokkaApp_class_instance_add_icon_method_assert_text_pytest():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    
    qa.add_icon("http://endpoint.pytest", "icon.png", "text.pytest")
    assert 'text.pytest' in appQk.config.get('ADMIN_ICONS')[0]


def test_QuokkaApp_class_instance_add_icon_method_assert_add_content_format():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    with pytest.raises(TypeError) as err:
        try:
            qa = QuokkaAdmin(
                appQk,
                index_view=IndexView(),
                template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
                base_template='admin/quokka/master.html'
            )
            qa.add_content_format()
            assert "takes 0 positional arguments but 1 was given" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_QuokkaApp_class_blueprint_property():
    assert appQk.blueprints != {}

def test_QuokkaApp_class_debug_property():
    assert appQk.debug == False

def test_QuokkaApp_class_env_property():
    assert appQk.env == 'production'

def test_QuokkaApp_class_extensions_property():
    assert appQk.extensions != {}

def test_QuokkaApp_class_got_first_request():
    assert appQk.got_first_request == False

def test_QuokkaApp_class_get_name_property():
    assert appQk.name == 'quokka'

def test_QuokkaApp_class_has_static_folder_property():
    assert appQk.has_static_folder == True



