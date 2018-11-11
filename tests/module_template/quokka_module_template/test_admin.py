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
    UserView, TweetForm,
    TweetView
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
tweet_view = TweetView(coll=mock_class_coll)


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


def test_class_UserView_action_disallowed_list():
    assert user_form.action_disallowed_list == []

def test_class_UserView_admin_property():
    assert user_form.admin is None

def test_class_UserView_blueprint_property():
    assert user_form.blueprint is None

def test_class_UserView_category_property():
    assert user_form.category is None

def test_class_UserView_details_modal_property():
    assert user_form.details_modal == False

def test_class_UserView_edit_modal_property():
    assert user_form.edit_modal == False

def test_class_UserView_endpoint_property():
    assert user_form.endpoint == 'quokka.module_template.quokka_module_template.admin.mock-collview'

def test_class_UserView_ajax_refs_property():
    assert user_form.form_ajax_refs is None

def test_class_UserView_form_columns_property():
    assert user_form.form_columns is None

def test_class_UserView_form_create_rules_property():
    assert user_form.form_create_rules is None

def test_class_UserView_url_property():
    assert user_form.url is None

def test_class_UserView_static_folder_property():
    assert user_form.static_folder is None

def test_class_UserView_simple_list_pager_property():
    assert user_form.simple_list_pager == False

def test_class_UserView_model_property():
    assert user_form.model is None

def test_class_UserView_name_property():
    assert user_form.name == 'Mock-Coll'

def test_class_UserView_page_size_property():
    assert user_form.page_size == 20

def test_class_UserView_static_url_path_property():
    assert user_form.static_url_path is None

def test_class_UserView_list_template_property():
    assert user_form.list_template == 'admin/model/list.html'

def test_class_UserView_form_rules_property():
    assert user_form.form_rules is None

def test_class_TweetForm():
 
    with pytest.raises(RuntimeError) as err:
        try:
            user_form = TweetForm()
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


def test_class_TweetView_is_instance():
    assert isinstance(tweet_view, TweetView) == True

def test_class_TweetView_action_disallowed_list():
    assert tweet_view.action_disallowed_list == []

def test_class_TweetView_admin_property():
    assert tweet_view.admin is None

def test_class_TweetView_blueprint_property():
    assert tweet_view.blueprint is None

def test_class_TweetView_category_property():
    assert tweet_view.category is None

def test_class_TweetView_details_modal_property():
    assert tweet_view.details_modal == False

def test_class_TweetView_edit_modal_property():
    assert tweet_view.edit_modal == False

def test_class_TweetView_endpoint_property():
    assert tweet_view.endpoint == 'quokka.module_template.quokka_module_template.admin.mock-collview'

def test_class_TweetView_ajax_refs_property():
    assert tweet_view.form_ajax_refs is None

def test_class_TweetView_form_columns_property():
    assert tweet_view.form_columns is None

def test_class_TweetView_form_create_rules_property():
    assert tweet_view.form_create_rules is None

def test_class_TweetView_url_property():
    assert tweet_view.url is None

def test_class_TweetView_static_folder_property():
    assert tweet_view.static_folder is None

def test_class_TweetView_simple_list_pager_property():
    assert tweet_view.simple_list_pager == False

def test_class_TweetView_model_property():
    assert tweet_view.model is None

def test_class_TweetView_name_property():
    assert tweet_view.name == 'Mock-Coll'

def test_class_TweetView_page_size_property():
    assert tweet_view.page_size == 20

def test_class_TweetView_static_url_path_property():
    assert tweet_view.static_url_path is None

def test_class_TweetView_list_template_property():
    assert tweet_view.list_template == 'admin/model/list.html'

def test_class_TweetView_form_rules_property():
    assert tweet_view.form_rules is None


