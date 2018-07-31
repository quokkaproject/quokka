import mock
import quokka
from quokka import create_app, create_app_base
from pytest_mock import mocker 
from quokka.core.app import QuokkaApp
from quokka.core.flask_dynaconf import configure_dynaconf

class MockTestApp(object):
    
    def __init__(self, config):
        self.config = config
        return self.config

def test_create_app(mocker):
    mocker.patch("quokka.create_app_base")
    mocker.patch("quokka.core.configure_extensions")
    create_app()
    quokka.create_app_base.assert_called_once_with(test=False)

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_QuokkaApp_called_is_false(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    quokka.create_app_base(test=False, ext_list=None)
    assert mock_QuokkaApp.called is False

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_dynaconf_called_is_false(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    quokka.create_app_base(test=False, ext_list=None)
    assert mock_configure_dynaconf.called is False

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_configure_extension_called_is_false(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    quokka.create_app_base(test=False, ext_list=None)
    assert mock_configure_extension.called is False

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_QuokkaApp_called_is_false_and_test_true(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    quokka.create_app_base(test=True, ext_list=[])
    assert mock_QuokkaApp.called is False

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_dynaconf_called_is_false_test_true_and_ext_list(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    quokka.create_app_base(test=True, ext_list=['quokka.core.configure_extension'])
    assert mock_configure_dynaconf.called is False

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_configure_dynaconf_called_is_true(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    list_ext = ['quokka.core.app.QuokkaApp', 
                'quokka.core.flask_dynaconf.configure_dynaconf',
                'quokka.core.configure_extension']
    quokka.create_app_base(test=True, ext_list=list_ext)
    assert mock_configure_dynaconf.called is True

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_QuokkaApp_called_is_true(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    list_ext = ['quokka.core.app.QuokkaApp', 
                'quokka.core.flask_dynaconf.configure_dynaconf',
                'quokka.core.configure_extension']
    quokka.create_app_base(test=True, ext_list=list_ext)
    assert mock_QuokkaApp.called is True

@mock.patch("quokka.core.app.QuokkaApp")
@mock.patch("quokka.core.flask_dynaconf.configure_dynaconf")
@mock.patch("quokka.core.configure_extension")
def test_create_app_base_function_configure_extension_called_is_true(mock_configure_extension, mock_configure_dynaconf, mock_QuokkaApp):
    list_ext = ['quokka.core.app.QuokkaApp', 
                'quokka.core.flask_dynaconf.configure_dynaconf',
                'quokka.core.configure_extension']
    quokka.create_app_base(test=True, ext_list=list_ext)
    assert mock_configure_extension.called is True


