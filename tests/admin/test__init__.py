import import_string
import pytest
import mock
import quokka
from flask_admin import Admin
from quokka.admin.views import FileAdmin, IndexView, ModelView
from quokka.admin import create_admin, QuokkaAdmin, configure_admin

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

#WIP:def 
@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_is_True(mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    pass
    #quokka.admin.configure_admin(app=mock_Admin, admin=None)
    #assert mock_create_admin.called is True
    #assert mock_create_admin.called is True








