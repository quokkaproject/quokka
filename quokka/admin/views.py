# coding: utf -8

from flask import current_app, redirect, url_for, abort
from flask_admin import AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin as _FileAdmin
from flask_admin.contrib.pymongo import ModelView as PyMongoModelView
from flask_simplelogin import is_logged_in
from quokka.admin.actions import CloneAction, PublishAction
from quokka.utils.routing import expose


class RequiresLogin(object):
    """login in admin"""
    def _handle_view(self, *args, **kwargs):  # noqa
        """Admin views requires login"""
        if current_app.config.get('ADMIN_REQUIRES_LOGIN') is True:
            if not is_logged_in():
                return redirect(
                    url_for('simplelogin.login', next="/admin")
                )


class FileAdmin(RequiresLogin, _FileAdmin):

    def __init__(self, *args, **kwargs):
        self.editable_extensions = kwargs.pop('editable_extensions', tuple())
        super(FileAdmin, self).__init__(*args, **kwargs)


class IndexView(RequiresLogin, AdminIndexView):

    @expose('/')
    def index(self):
        if not current_app.config.get('SECRET_KEY'):
            return abort(
                500,
                '/admin requires the "SECRET_KEY" config var to be set in '
                '.secrets.yml or quokka.yml e.g: '
                'QUOKKA: {"SECRET_KEY": "secret-key"} '
                'or exported as `export QUOKKA_SECRET_KEY="secret-key"'
            )
        limit = current_app.config.get('ADMIN_INDEX_CONTENT_LIMIT', 8)
        sort = current_app.config.get(
            'ADMIN_INDEX_CONTENT_SORT', [('date', -1)])
        contents = current_app.db.content_set(limit=limit, sort=sort)
        return self.render('admin/index.html', contents=contents)


class ModelView(CloneAction, PublishAction,
                RequiresLogin,
                PyMongoModelView):
    """Base model view for all contents"""

    page_size = 20
    can_set_page_size = True

    def _get_endpoint(self, endpoint):
        if not endpoint:
            endpoint = self.__class__.__name__.lower()
        endpoint = f'{self.__module__}.{endpoint}'
        return endpoint
