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
        #todo: apply code to remove: cli-test-file
        
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    except RuntimeError:
        raise

#https://semaphoreci.com/community/tutorials/getting-started-with-mocking-in-python
#https://github.com/pytest-dev/pytest-mock
#https://medium.com/@bfortuner/python-unit-testing-with-pytest-and-mock-197499c4623c
#TypeError: test_check() takes 1 positional argument but 2 were given


class AppMock():

    def __init__(param):
        return None
    
    def extensions():
        pass
    
    def blueprints():
        pass


#criar mock para:
#@cli.command()
#@with_app
@mock.patch("manage.cli")
@mock.patch("quokka.cli.with_app")
@mock.patch("quokka.cli.click")
@mock.patch("pprint.pprint")
def test_check(mock_pprint, mock_click, mock_with_app, mock_cli):
    app = AppMock()
    check(app)
    mock_click.echo.assert_called_with("App.")


#@mock.patch("functools.wraps")
#@mock.patch("quokka.cli.decorator")
#@mock.patch("quokka.create_app")
#def test_with_app(mock_create_app, mock_wraps):
    #with_app('f')
    #assert mock_wraps.wraps.called is True

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


