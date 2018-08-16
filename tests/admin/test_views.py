import pytest
import mock
import json
from flask import current_app, redirect, url_for, abort
from flask_admin import AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin as _FileAdmin
from flask_admin.contrib.pymongo import ModelView as PyMongoModelView
from flask_simplelogin import is_logged_in
from quokka.admin.actions import CloneAction, PublishAction
from quokka.utils.routing import expose
from quokka.admin.views import RequiresLogin, FileAdmin, IndexView, ModelView

#pytest - fixtures - setUp();
rl = RequiresLogin()
fa = FileAdmin("/home/")
#class IndexView(RequiresLogin, AdminIndexView):
iv = IndexView() 
#class ModelView(CloneAction, PublishAction, RequiresLogin, PyMongoModelView):
#mv = ModelView()

def test_RequiresLogin_class_is_instance_of():
    assert isinstance(rl, RequiresLogin) == True

def test_FileAdmin_class_instance_of_None_param_base_path():
    with pytest.raises(TypeError) as err:
        try:
            fa = FileAdmin()
            assert "missing 1 required positional argument:" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        
        
        except RuntimeError:
            raise

        except Exception:
            raise

def test_FileAdmin_class_instance_of_param_base_path_dont_exists_or_inaccessible():
    with pytest.raises(OSError) as err:
        try:
            fa = FileAdmin("/home/quokka")
            assert "does not exist or is not accessible" in str(err.value)

        except FileExistsError:
            raise        
        
        except RuntimeError:
            raise
        
        except TypeError:
            raise

        except Exception:
            raise


def test_FileAdmin_class_is_instance_of():
    assert isinstance(fa, FileAdmin) == True

def test_FileAdmin_class_property_date_format():
    assert fa.date_format == '%Y-%m-%d %H:%M:%S'

def test_FileAdmin_class_property_default_desc():
    assert fa.default_desc == 0

def test_FileAdmin_class_property_base_url_None():
    assert fa.base_url == None

def test_FileAdmin_class_property_admin_None():
    assert fa.admin == None

def test_FileAdmin_class_property_url_None():
    assert fa.url == None

def test_FileAdmin_class_property_allowed_extensions_None():
    assert fa.allowed_extensions == None

def test_FileAdmin_class_property_blueprint_None():
    assert fa.blueprint == None

def test_FileAdmin_class_property_category_None():
    assert fa.category == None

def test_FileAdmin_class_property_endpoint():
    assert fa.endpoint == 'fileadmin'

def test_FileAdmin_class_property_name():
    assert fa.name == None

def test_FileAdmin_class_property_column_list():
    assert fa.column_list == ('name', 'size', 'date')

def test_FileAdmin_class_property_upload_template():
    assert fa.upload_template == 'admin/file/form.html'

def test_FileAdmin_class_property_upload_menu():
    assert fa.menu == None

def test_FileAdmin_class_property_list_template():
    assert fa.list_template == 'admin/file/list.html'

def test_FileAdmin_class_property_menu_class_name():
    assert fa.menu_class_name == None

def test_FileAdmin_class_property_can_delete():
    assert fa.can_delete == True

def test_FileAdmin_class_property_can_delete_dirs():
    assert fa.can_delete_dirs == True

def test_FileAdmin_class_property_can_download():
    assert fa.can_download == True

def test_FileAdmin_class_property_can_download():
    assert fa.can_download == True

def test_FileAdmin_class_property_can_mkdir():
    assert fa.can_mkdir == True

def test_FileAdmin_class_property_can_rename():
    assert fa.can_rename == True

def test_FileAdmin_class_property_can_upload():
    assert fa.can_upload == True

def test_FileAdmin_class_property_column_labels_dict():
    assert fa.column_labels == {'name': 'Name', 'size': 'Size', 'date': 'Date'}



def test_IndexView():
    pass

def test_ModelView():
    pass



