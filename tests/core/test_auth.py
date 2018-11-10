import pytest
import mock
import click
import getpass
from flask import (
    current_app, url_for, Markup
)
from flask_htmlbuilder.htmlbuilder import html
from quokka.admin.actions import (
    UserProfileBlockAction
)
from quokka.admin.views import (
    ModelView
)
from quokka.admin.forms import (
    Form, fields, 
    ValidationError, validators
)
from quokka.utils.text import (
    slugify
)
from werkzeug.security import (
    check_password_hash, 
    generate_password_hash
)
from flask_simplelogin import (
    SimpleLogin, get_username
)
from quokka.core.auth import (
    create_user, UserForm,
    format_profile, UserView,
    validate_login, configure,
    configure_user_admin, get_current_user
)

################################################################################
#pytest - fixtures                                                             #
################################################################################
param_data = {'username': 'mock-user', 'password':'mock-pass'}


#################################################################################
#pytest - Quokka - tests/core/test_app.py                                       #
#################################################################################
def test_create_user():

    with pytest.raises(ValueError) as err:
        try:
            debugger = create_user(data=param_data)
            assert "username and password are required." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_class_UserForm():
    
    with pytest.raises(RuntimeError) as err:
        try:
            userform = UserForm()
            assert "Working outside of application context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


