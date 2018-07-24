import quokka
from quokka import create_app, create_app_base
from pytest_mock import mocker 

class MockTestApp(object):
    
    def __init__(self, config):
        self.config = config
        return self.config

#def test_version_quokka():
    #assert quokka.__version__ == '0.3.4'

def test_create_app(mocker):
    mocker.patch("quokka.create_app_base")
    mocker.patch("quokka.core.configure_extensions")
    create_app()
    quokka.create_app_base.assert_called_once_with(test=False)

"""
#needs to config a function with get;
def test_create_app_base(mocker):
#    app = MockTestApp(object)
#    app.config.get(
#        SETTINGS_MODULE='test',
#        ENVMODE='test',
#        BABEL_DEFAULT_LOCALE='test',
#    )
    
#    app.config.logger(
#        SETTINGS_MODULE='test',
#        ENVMODE='test',
#    )
#    
#    app.jinja_env(
#        SETTINGS_MODULE='test',
#        ENVMODE='test',
#    )
#    
#    app.jinja_env.extensions(
#        SETTINGS_MODULE='test',
#        ENVMODE='test',
#    )

    mocker.patch("quokka.core.app.QuokkaApp")
    mocker.patch("quokka.core.configure_extension")
    mocker.patch("quokka.core.flask_dynaconf.configure_dynaconf")
#    mocker.patch("app.config.get")
    create_app_base()
    quokka.core.app.QuokkaApp.assert_called_once_with('quokka')
    quokka.core.flask_dynaconf.configure_dynaconf.assert_called_once_with(app)
#    app.config.get.assert_called_once_with()
"""

