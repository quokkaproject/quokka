# coding : utf -8

from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.admin import AdminIndexView
from flask.ext.admin.actions import action
from flask.ext.security import current_user
from flask.ext.security.utils import url_for_security
from flask import redirect


class Roled(object):

    def is_accessible(self):

        roles_accepted = getattr(self, 'roles_accepted', None)
        if roles_accepted:
            accessible = any(
                [current_user.has_role(role) for role in roles_accepted]
            )
            return accessible
        return True

    def _handle_view(self, name, *args, **kwargs):
        if not current_user.is_authenticated():
            return redirect(url_for_security('login', next="/admin"))
        if not self.is_accessible():
            return self.render("admin/denied.html")


class ModelAdmin(Roled, ModelView):

    @action('toggle_publish', 'Publish/Unpublish', 'Publish/Unpublish?')
    def action_merge(self, ids):
        for i in ids:
            instance = self.model.objects.get(id=i)
            instance.published = not instance.published
            instance.save()


class BaseIndexView(Roled, AdminIndexView):
    pass
