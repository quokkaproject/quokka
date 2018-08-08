import import_string
import pytest
import mock
import quokka
from flask_admin import Admin
from quokka.admin.views import FileAdmin, IndexView, ModelView
from quokka.admin import create_admin, QuokkaAdmin, configure_admin
from quokka.core.app import QuokkaApp
from quokka.core.flask_dynaconf import configure_dynaconf    


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_failed_param_app_None_err(mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.create_admin(app=None)
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_failed_param_app_string_empty_err(mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.create_admin(app="")
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_called_IndexView_False(mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    quokka.admin.create_admin(app=mock_Admin)
    assert mock_IndexView.called is False


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_called_QuokkaAdmin_False(mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    quokka.admin.create_admin(app=mock_Admin)
    assert mock_QuokkaAdmin(app=mock_Admin).called is False


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_called_QuokkaAdmin_is_not_None(mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    resp = quokka.admin.create_admin(app=appQk)
    assert resp is not None


def test_create_admin_called_QuokkaAdmin_is_instance_resp_name_admin():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    resp = quokka.admin.create_admin(app=appQk)
    assert resp.name == 'Admin' 

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_admin_called_param_app_None_err(mock_create_admin, mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.configure_admin(app=None, admin=None)
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_admin_called_param_app_string_empty_err(mock_create_admin, mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.configure_admin(app="", admin=None)
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_None_assert_True(mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    quokka.admin.configure_admin(app=appQk, admin=None)
    assert mock_create_admin.called is True

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_mock_quokka_admin_assert_False(mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    quokka.admin.configure_admin(app=appQk, admin=mock_QuokkaAdmin)
    assert mock_create_admin.called is False

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_None_assert_is_not_None(mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    resp = quokka.admin.configure_admin(app=appQk, admin=None)
    assert resp != None

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_None_assert_is_Quokka_Admin_instance(mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQkk = QuokkaApp('quokka')
    configure_dynaconf(appQkk)
    resp = quokka.admin.configure_admin(app=appQkk, admin=None)
    assert resp.name == 'Quokka Admin'

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_file_admin_called_param_app_None_err(mock_create_admin, mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.configure_file_admin(app=None)
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_file_admin_called_param_app_string_empty_err(mock_create_admin, mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.configure_file_admin(app="")
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_file_admin_called_param_admin_None_assert_None(mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    assert quokka.admin.configure_file_admin(app=appQk) is None



@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_extra_views_called_param_app_None_err(mock_create_admin, mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.configure_extra_views(app=None)
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_extra_views_called_param_app_string_empty_err(mock_create_admin, mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    
    with pytest.raises(AttributeError) as err:
        try:
            quokka.admin.configure_extra_views(app="")
            assert "object has no attribute" in str(err.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_extra_views_called_param_admin_None_assert_None(mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    assert quokka.admin.configure_extra_views(app=appQk) is None







