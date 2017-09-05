
import json
import random
from copy import deepcopy

from flask import Response, current_app, flash, redirect, url_for
from flask_admin.actions import action


class PublishAction(object):
    @action(
        'toggle_publish',
        'Publish/Unpublish',
        'Publish/Unpublish?'
    )
    def action_toggle_publish(self, ids):
        for _id in ids:
            model = current_app.db.get_with_content(_id=_id)
            model['published'] = not model['published']
            # fires the versioning and hooks
            self._on_model_change(None, model, False)

            pk = self.get_pk_value(model)
            self.coll.update({'_id': pk}, model)

            # more hooks
            self.after_model_change(None, model, False)
        flash(
            f'{len(ids)} items were successfully published/Unpublished.',
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

        model = current_app.db.get_with_content(_id=ids[0])
        clone = deepcopy(model)
        del clone['_id']
        clone['slug'] = f'{clone["slug"]}-{random.getrandbits(32)}'
        clone['_isclone'] = True
        self._on_model_change(None, clone, True)
        self.coll.insert(clone)
        self.after_model_change(None, clone, True)
        return redirect(url_for('.edit_view', id=clone['_id']))


# TODO: Serialize and activate thia action
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
