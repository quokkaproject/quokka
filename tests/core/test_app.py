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


#################################################################################
#pytest - Quokka - tests/core/test_app.py                                       #
#################################################################################

def test_class_QuokkaApp():
    pass
    

def test_class_QuokkaModule():
    pass
    


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







