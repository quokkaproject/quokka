
import datetime
import json
import random

from flask import Response, flash, redirect, url_for
from flask_admin.actions import action


class PublishAction(object):
    @action(
        'toggle_publish',
        'Publish/Unpublish',
        'Publish/Unpublish?'
    )
    def action_toggle_publish(self, ids):
        for i in ids:
            instance = self.get_instance(i)
            instance.published = not instance.published
            instance.save()
        count = len(ids)
        flash(
            f'{count} items were successfully published/Unpublished.',
            'success'
        )


class CloneAction(object):
    @action(
        'clone_item',
        'Create a copy',
        'Are you sure you want a copy?'
    )
    def action_clone_item(self, ids):
        if len(ids) > 1:
            flash(
                "You can select only one item for this action",
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
    @action('export_to_json', 'Export as json')
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

    @action('export_to_csv', 'Export as csv')
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
