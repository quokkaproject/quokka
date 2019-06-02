import import_string
import pytest
import mock
import quokka
from flask_admin import Admin
from quokka.admin.views import FileAdmin, IndexView, ModelView
from quokka.admin import create_admin, QuokkaAdmin, configure_admin
from quokka.core.app import QuokkaApp
from quokka.core.flask_dynaconf import configure_dynaconf

###################################################
# pytest - Quokka - quokka/admin/test__init__.py  #
###################################################
@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_failed_param_app_none_err(mock_Admin,
        mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.create_admin(app=None)
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_failed_param_app_string_empty_err(mock_Admin,
        mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.create_admin(app="")
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_called_indexview_false(mock_Admin,
        mock_QuokkaAdmin, mock_IndexView):
    quokka.admin.create_admin(app=mock_Admin)
    assert mock_IndexView.called is False


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_called_quokkaadmin_false(mock_Admin,
        mock_QuokkaAdmin, mock_IndexView):
    quokka.admin.create_admin(app=mock_Admin)
    assert mock_QuokkaAdmin(app=mock_Admin).called is False


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_called_quokkaapp_is_instance_of(mock_Admin,
        mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    assert isinstance(appQk, QuokkaApp) == True


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_create_admin_called_quokkaadmin_is_not_none(mock_Admin,
        mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    resp = quokka.admin.create_admin(app=appQk)
    assert resp is not None


def test_create_admin_called_quokkaadmin_is_instance_resp_name_admin():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    resp = quokka.admin.create_admin(app=appQk)
    assert resp.name == 'Admin'


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_admin_called_param_app_none_err(mock_create_admin,
        mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.configure_admin(app=None, admin=None)
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_admin_called_param_app_string_empty_err(mock_create_admin,
        mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.configure_admin(app="", admin=None)
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_none_assert_true(mock_Admin,
        mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    quokka.admin.configure_admin(app=appQk, admin=None)
    assert mock_create_admin.called is True


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_mock_quokka_admin_assert_false(mock_Admin,
        mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    quokka.admin.configure_admin(app=appQk, admin=mock_QuokkaAdmin)
    assert mock_create_admin.called is False


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_none_assert_is_not_none(mock_Admin,
        mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    resp = quokka.admin.configure_admin(app=appQk, admin=None)
    assert resp != None


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_admin_called_param_admin_none_assert_is_quokka_admin_instance(
        mock_Admin, mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQkk = QuokkaApp('quokka')
    configure_dynaconf(appQkk)
    resp = quokka.admin.configure_admin(app=appQkk, admin=None)
    assert resp.name == 'Quokka Admin'


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_file_admin_called_param_app_none_err(mock_create_admin,
        mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.configure_file_admin(app=None)
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_file_admin_called_param_app_string_empty_err(mock_create_admin,
        mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.configure_file_admin(app="")
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_file_admin_called_param_admin_none_assert_none(mock_Admin,
        mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    assert quokka.admin.configure_file_admin(app=appQk) is None


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_extra_views_called_param_app_none_err(mock_create_admin,
        mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.configure_extra_views(app=None)
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
@mock.patch("quokka.admin.create_admin")
def test_configure_extra_views_called_param_app_string_empty_err(mock_create_admin,
        mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        quokka.admin.configure_extra_views(app="")
        assert "object has no attribute" in str(err.value)


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("quokka.admin.create_admin")
@mock.patch("flask_admin.Admin")
def test_configure_extra_views_called_param_admin_none_assert_none(mock_Admin,
        mock_create_admin, mock_QuokkaAdmin, mock_IndexView):
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    assert quokka.admin.configure_extra_views(app=appQk) is None


@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
@mock.patch("flask_admin.Admin")
def test_quokkaadmin_class_instance_error(mock_Admin, mock_QuokkaAdmin, mock_IndexView):
    with pytest.raises(AttributeError) as err:
        qa = QuokkaAdmin(Admin)
        assert "type object 'Admin' has no attribute" in str(err.value)


def test_quokkaadmin_class_is_instance_of():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)

    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    assert isinstance(qa, QuokkaAdmin) == True


def test_quokkaadmin_class_instance_register_method():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    assert qa.name == "Admin"


def test_quokkaadmin_class_instance_add_icon_method_assert_endpoint():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    
    qa.add_icon("http://endpoint.pytest", "icon.png", "text.pytest")
    assert 'http://endpoint.pytest' in appQk.config.get('ADMIN_ICONS')[0]


def test_quokkaadmin_class_instance_add_icon_method_assert_icon():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    
    qa.add_icon("http://endpoint.pytest", "icon.png", "text.pytest")
    assert 'icon.png' in appQk.config.get('ADMIN_ICONS')[0]


def test_quokkaadmin_class_instance_add_icon_method_assert_text_pytest():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    qa = QuokkaAdmin(
        appQk,
        index_view=IndexView(),
        template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
        base_template='admin/quokka/master.html'
    )
    
    qa.add_icon("http://endpoint.pytest", "icon.png", "text.pytest")
    assert 'text.pytest' in appQk.config.get('ADMIN_ICONS')[0]


def test_QuokkaAdmin_class_instance_add_icon_method_assert_add_content_format():
    appQk = QuokkaApp('quokka')
    configure_dynaconf(appQk)
    
    with pytest.raises(TypeError) as err:
        qa = QuokkaAdmin(
            appQk,
            index_view=IndexView(),
            template_mode=appQk.config.get('FLASK_ADMIN_TEMPLATE_MODE'),
            base_template='admin/quokka/master.html'
        )
        qa.add_content_format()
        assert "takes 0 positional arguments but 1 was given" in str(err.value)

