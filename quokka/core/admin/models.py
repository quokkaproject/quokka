# coding : utf -8
import json
import random
import datetime

from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.admin.babel import gettext, ngettext, lazy_gettext
from flask.ext.admin import AdminIndexView
from flask.ext.admin.actions import action
from flask.ext.security import current_user
from flask.ext.security.utils import url_for_security
from flask import redirect, flash, url_for, Response

from quokka.modules.accounts.models import User


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

    form_subdocuments = {}

    def get_instance(self, i):
        try:
            return self.model.objects.get(id=i)
        except self.model.DoesNotExist:
            flash(gettext("Item not found %(i)s", i=i), "error")

    @action('toggle_publish',
            lazy_gettext('Publish/Unpublish'),
            lazy_gettext('Publish/Unpublish?'))
    def action_toggle_publish(self, ids):
        for i in ids:
            instance = self.get_instance(i)
            instance.published = not instance.published
            instance.save()
        count = len(ids)
        flash(ngettext('Item successfully published/Unpublished.',
                       '%(count)s items were successfully'
                       ' published/Unpublished.',
              count,
              count=count))

    @action('clone_item',
            lazy_gettext('Create a copy'),
            lazy_gettext('Are you sure you want a copy?'))
    def action_clone_item(self, ids):
        if len(ids) > 1:
            flash(gettext("You can select only one item for this action"),
                  'error')
            return

        instance = self.get_instance(ids[0])
        new = instance.from_json(instance.to_json())
        new.id = None
        new.published = False
        new.last_updated_by = User.objects.get(id=current_user.id)
        new.updated_at = datetime.datetime.now()
        new.slug = "{0}-{1}".format(new.slug, random.getrandbits(32))
        new.save()

        return redirect(url_for('.edit_view', id=new.id))

    @action('export_to_json', lazy_gettext('Export as json'))
    def export_to_json(self, ids):
        qs = self.model.objects(id__in=ids)

        return Response(
            qs.to_json(),
            mimetype="text/json",
            headers={
                "Content-Disposition":
                "attachment;filename=%s.json" % self.model.__name__.lower()
            }
        )

    @action('export_to_csv', lazy_gettext('Export as csv'))
    def export_to_csv(self, ids):
        qs = json.loads(self.model.objects(id__in=ids).to_json())

        def generate():
            yield ','.join(list(qs[0].keys())) + '\n'
            for item in qs:
                yield ','.join([str(i) for i in list(item.values())]) + '\n'

        return Response(
            generate(),
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                "attachment;filename=%s.csv" % self.model.__name__.lower()
            }
        )


class BaseIndexView(Roled, AdminIndexView):
    pass
