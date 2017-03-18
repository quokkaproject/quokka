
import datetime
import random
import json
from flask import flash, redirect, url_for, Response
from flask_admin.actions import action
from quokka.admin.utils import _, _l, _n


class PublishAction(object):
    @action(
        'toggle_publish',
        _l('Publish/Unpublish'),
        _l('Publish/Unpublish?')
    )
    def action_toggle_publish(self, ids):
        for i in ids:
            instance = self.get_instance(i)
            instance.published = not instance.published
            instance.save()
        count = len(ids)
        flash(_n('Item successfully published/Unpublished.',
                 '%(count)s items were successfully published/Unpublished.',
                 count,
                 count=count))


class CloneAction(object):
    @action(
        'clone_item',
        _l('Create a copy'),
        _l('Are you sure you want a copy?')
    )
    def action_clone_item(self, ids):
        if len(ids) > 1:
            flash(
                _("You can select only one item for this action"),
                'error'
            )
            return

        instance = self.get_instance(ids[0])
        new = instance.from_json(instance.to_json())
        new.id = None
        new.published = False
        new.last_updated_by = None  # User.objects.get(id=current_user.id)
        new.updated_at = datetime.datetime.now()
        new.slug = "{0}-{1}".format(new.slug, random.getrandbits(32))
        new.save()
        return redirect(url_for('.edit_view', id=new.id))


class ExportAction(object):
    @action('export_to_json', _l('Export as json'))
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

    @action('export_to_csv', _l('Export as csv'))
    def export_to_csv(self, ids):
        qs = json.loads(self.model.objects(id__in=ids).to_json())

        def generate():
            yield ','.join(list(max(qs, key=lambda x: len(x)).keys())) + '\n'
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
