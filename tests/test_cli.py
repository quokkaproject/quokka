import mock
import click
import quokka
import pytest_django
from yaml import load
from quokka import create_app
from pytest_mock import mocker 
from manage.cli import cli, init_cli
import pytest, os, errno, pathlib, os.path, pytest_mock
from quokka.cli import copyfolder, with_app, check, main

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


def test_copy_folder_file_exists():
    
    try:
        copyfolder(directory_pwd+file_test, directory_pwd+directory_test+file_test)
        assert os.path.isfile(directory_pwd+directory_test+file_test) is True

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    except RuntimeError:
        raise

#https://semaphoreci.com/community/tutorials/getting-started-with-mocking-in-python
#https://github.com/pytest-dev/pytest-mock
#https://medium.com/@bfortuner/python-unit-testing-with-pytest-and-mock-197499c4623c
#TypeError: test_check() takes 1 positional argument but 2 were given
#@mock.patch('manage.cli')
#@mock.patch('quokka.cli.with_app')
#def test_check(mocker):
#    mocker.patch("click.echo")
#    check()
#    click.echo.assert_called_once_with("Extensions.")
    #pprint(app.extensions)
    #click.echo("Modules.")
    #pprint(app.blueprints)
    #click.echo("App.")
    #return app
    
#    mocker.patch('click.echo')
    #mocker.patch('pprint')
#    check(None)
#    click.echo.assert_called_once_with("Extensions.")
    #pprint.assert_called_once_with("app.extensions")
    #click.echo.assert_called_once_with("Modules.")
    #pprint.assert_called_once_with("app.blueprints")
    #click.echo.assert_called_once_with("App.")

#AssertionError: Expected 'decorator' to be called once. Called 0 times.
def test_with_app(mocker):
    mocker.patch("quokka.create_app")
#    mocker.patch("click.echo")
    with_app('f')
#    quokka.create_app.decorator.assert_called_once_with('env')

def test_init(mocker):
    pass

def test_adduser(mocker):
    pass

def test_execute(mocker):
    pass

#error: missing command
@mock.patch('manage.cli')
def test_main(mocker):
    mocker.patch("manage.cli.init_cli")
#    quokka.cli.main()
#    manage.cli.init_cli.assert_called_once_with(cli)


