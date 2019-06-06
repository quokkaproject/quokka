
import json
import random
from copy import deepcopy
from datetime import datetime

from flask import Markup
from flask import Response, current_app, flash, redirect, url_for
from flask_admin.actions import action

from quokka.utils.text import slugify


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


class UserProfileBlockAction(object):
    @action(
        'create_userprofile',
        'Create user profile block',
        'Are you sure you want to create user profile block?'
    )
    def action_create_userprofile(self, ids):
        for _id in ids:
            user = current_app.db.users.find_one({'_id': _id})
            if not user.get('fullname'):
                user['fullname'] = user['username']
                current_app.db.users.update_one(
                    {'_id': user['_id']}, {'fullname': user['fullname']}
                )
                # This update looks like having a cache
                # self.coll.update_one(
                #     {'_id': _id}, {'fullname': user['fullname']}
                # )
            fullslug = slugify(user['fullname'])
            existing_block = current_app.db.get(
                'index', {'content_type': 'block', 'slug': fullslug}
            )

            # fix vulnerabillity here
            # test sanity variables values

            if existing_block:
                blocklink = url_for(
                    'quokka.core.content.admin.blockview.edit_view',
                    id=existing_block['_id']
                )
                flash(Markup(
                    f'Profile block for {user["username"]} '
                    f'already exists at: '
                    f'<a href="{blocklink}">{existing_block["_id"]}</a>'
                ))
            else:
                # TODO: move creation logic to a model like obj
                new_data = {
                    'title': user['fullname'],
                    'slug': fullslug,
                    'summary': f'Profile page for {user["username"]}',
                    'published': True,
                    'comments': False,
                    'content_type': 'block',
                    'version': 0,
                    'date': datetime.now(),
                    'modified': datetime.now(),
                    'language': 'en',
                    'content_format': 'markdown',
                    'created_by': 'admin',
                    'modified_by': 'admin',
                    'category': '',
                    'category_slug': '',
                    'custom_vars': [
                        {'key': 'profile_title',
                         'value': f'@note change this field to customize html page title'},  # noqa
                        {'key': 'twitter',
                         'value': f'@note Fill this field with user twitter profile e.g: http://twitter.com/{user["username"]}'},  # noqa
                        {'key': 'facebook',
                         'value': f'@note Fill this field with user facebook profile e.g: http://facebook.com/{user["username"]}'},  # noqa
                        {'key': 'pinterest',
                         'value': f'@note Fill this field with user pinterest profile e.g: http://pinterest.com/{user["username"]}'},  # noqa
                        {'key': 'github',
                         'value': f'@note Fill this field with user github profile e.g http://github.com/{user["username"]}'},  # noqa
                        {'key': 'aboutme',
                         'value': f'@note Fill this field with user about.me profile e.g: http://aboutme.com/{user["username"]}'},  # noqa
                        {'key': 'instagram',
                         'value': f'@note Fill this field with user instagram profile e.g: http://instagram.com/{user["username"]}'},  # noqa
                        {'key': 'site',
                         'value': '@note Fill this field with user website link'},  # noqa
                        {'key': 'banner_color', 'value': '@note Fill this field with a color code or name e.g: #ffcc00 or yellow'},  # noqa
                        {'key': 'banner_image', 'value': '@note Fill this field witha banner image url e.g: http://site.com/image.jpg'},  # noqa
                        {'key': 'gravatar_email', 'value': '@note Fill this field with gravatar registered email e.g: user@site.com'},  # noqa
                        {'key': 'author_avatar', 'value': '@note Fill this field with an absolute url to a profile image e.g: http://site.com/image.png'},  # noqa
                    ],
                    'quokka_create_form_class': 'FormMeta',
                    'quokka_create_form_module': 'quokka.core.content.formats',
                    'quokka_format_class': 'MarkdownFormat',
                    'quokka_format_module': 'quokka.core.content.formats',
                    'quokka_module': 'quokka.core.content.admin',
                    'tags_slug': None,
                    'block_items': [],
                    'authors_slug': None,
                }
                new = current_app.db.insert('index', new_data)
                new_data['_id'] = new.inserted_id
                current_app.db.push_content(new_data)
                newlink = url_for(
                    'quokka.core.content.admin.blockview.edit_view',
                    id=new.inserted_id
                )
                flash(Markup(
                    f'Profile block for {user["username"]} '
                    f'Created at: '
                    f'<a href="{newlink}">{new.inserted_id}</a>'
                ))


# TODO: Serialize and activate this action
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
