import pytest
import mock
from flask import current_app
from flask_admin.contrib.pymongo import filters
from flask_admin.form import Select2Widget
from flask_admin.model.fields import (
    InlineFieldList, InlineFormField
)
from quokka.admin.forms import Form, fields
from quokka.admin.views import ModelView
from quokka.module_template.quokka_module_template.admin import (
    InnerForm, UserForm, 
    UserView, TweetForm
)


################################
#pytest - fixtures             #
################################
class MockClassColl():
    name=None          
    def __init__(self):  
        self.name = "mock-coll"

mock_class_coll = MockClassColl()
user_form = UserView(coll=mock_class_coll)

#####################################
#pytest - Quokka - test__init__.py  #
#####################################
def test_class_InnerForm():

    with pytest.raises(RuntimeError) as err:
        try:
            inner_form = InnerForm()
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


def test_class_UserForm():

    with pytest.raises(RuntimeError) as err:
        try:
            user_form = UserForm()
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



def test_class_UserView():
    pass


def test_class_TweetForm():
    pass

def test_class_TweetView():
    pass

