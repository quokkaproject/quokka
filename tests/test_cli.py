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
from click.testing import CliRunner
from pathlib import Path

################################
#pytest - fixtures - setUp();  #
################################
directory_pwd = os.getcwd()+"/tests/"
directory_test = "copy-directory-test/"
file_test = "cli-test-file"

class AppMock():

    def __init__(param):
        return None
    
    def extensions():
        pass
    
    def blueprints():
        pass

#pytest - fixture click.testing
@pytest.fixture(scope='function')
def runner(request):
    return CliRunner()


#################################
#pytest - Quokka - test_cli.py  #
#################################
def test_copy_folder_error_first_param():
    with pytest.raises(FileNotFoundError) as error:
        try:
            copyfolder("", directory_pwd+directory_test+file_test)
            assert "No such file or directory" in str(error.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise        

        except Exception:
            raise

def test_copy_folder_error_second_param():
    with pytest.raises(FileNotFoundError) as error:
        try:
            copyfolder(directory_pwd+file_test, "")        
            assert "No such file or directory" in str(error.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_copy_folder_file_exists():
    try:
        copyfolder(directory_pwd+file_test, directory_pwd+directory_test+file_test)
        assert os.path.isfile(directory_pwd+directory_test+file_test) is True
        os.unlink(directory_pwd+directory_test+file_test)
        
    except TypeError as e:
        assert 'nargs=-1' in str(e)

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    except RuntimeError:
        raise

    except FileExistsError:
        raise        

    except Exception:
        raise


@mock.patch("functools.wraps")
@mock.patch("quokka.create_app")
def test_with_app(mock_create_app, mock_wraps):
    with_app('f')
    assert mock_wraps.called is False

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

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    except RuntimeError:
        raise

    except FileExistsError:
        raise        

    except Exception:
        raise


