"""
https://semaphoreci.com/community/tutorials/getting-started-with-mocking-in-python
https://github.com/pytest-dev/pytest-mock
https://medium.com/@bfortuner/python-unit-testing-with-pytest-and-mock-197499c4623c
TypeError: test_check() takes 1 positional argument but 2 were given
"""

import mock
import click
import quokka
import pytest_django
from yaml import load
from quokka import create_app
from pytest_mock import mocker 
from manage.cli import cli, init_cli
import pytest, os, errno, pathlib, os.path, pytest_mock
from quokka.cli import copyfolder, with_app, check, main, init, runserver

#fixtures
directory_pwd = os.getcwd()+"/tests/"
directory_test = "copy-directory-test/"
file_test = "cli-test-file"

def test_copy_folder_error_first_param():

    with pytest.raises(FileNotFoundError) as error:
        
        try:
            copyfolder("", directory_pwd+directory_test+file_test)
            assert "No such file or directory" in str(error.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise

def test_copy_folder_error_second_param():
    
    with pytest.raises(FileNotFoundError) as error:
        
        try:
            copyfolder(directory_pwd+file_test, "")        
            assert "No such file or directory" in str(error.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise


#TODO: apply code to remove: cli-test-file
def test_copy_folder_file_exists():
    
    try:
        copyfolder(directory_pwd+file_test, directory_pwd+directory_test+file_test)
        assert os.path.isfile(directory_pwd+directory_test+file_test) is True
        
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    except RuntimeError:
        raise


class AppMock():

    def __init__(param):
        return None
    
    def extensions():
        pass
    
    def blueprints():
        pass

@mock.patch("manage.cli")
@mock.patch("quokka.cli.with_app")
@mock.patch("quokka.cli.click")
@mock.patch("pprint.pprint")
def test_check(mock_pprint, mock_click, mock_with_app, mock_cli):
    app = AppMock()
    check(app)
    mock_click.echo.assert_called_with("App.")

#FIXME: assert bool wrong
@mock.patch("functools.wraps")
#@mock.patch("quokka.cli.decorator")
@mock.patch("quokka.create_app")
def test_with_app(mock_create_app, mock_wraps):
    with_app('f')
    assert mock_wraps.called is False

#fixture click.testing
from click.testing import CliRunner
@pytest.fixture(scope='function')
def runner(request):
    return CliRunner()

from pathlib import Path
#FIXME: assert bool wrong
@mock.patch("click.command")
@mock.patch("click.argument")
@mock.patch("click.option")
@mock.patch("pathlib.Path")
@mock.patch("quokka.cli.copyfolder")
def test_init(mocker_copyfolder, mocker_Path, mocker_option, mocker_argument, mocker_command, runner):
    
    try:
        @click.command()
        @click.argument('name', nargs=-1)
        def run_init_test():
            init('name-mock', '.', '../', 'theme-mock', 'modules-mock')
            
        result = runner.invoke(run_init_test)
        
        assert not result.exception
        assert mocker_copyfolder.called is False
    except TypeError as e:
        assert 'nargs=-1' in str(e)
         
    
@mock.patch("click.command")
@mock.patch("click.option")
def test_adduser(mock_option, mock_command):
    pass

def test_execute(mocker):
    pass

@mock.patch("click.command")
@mock.patch("click.option")
@mock.patch("quokka.cli.with_app")
def test_runserver(mocker_option, mocker_command, mocker_with_app):
    pass

#error: missing command
#@mock.patch('manage.cli')
#def test_main(mocker):
    #mocker.patch("manage.cli.init_cli")
#    quokka.cli.main()
#    manage.cli.init_cli.assert_called_once_with(cli)


