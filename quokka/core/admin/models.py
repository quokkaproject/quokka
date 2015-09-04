# coding : utf -8
import json
import random
import datetime

from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin as _FileAdmin
from flask.ext.admin.babel import gettext, ngettext
from flask.ext.admin import AdminIndexView
from flask.ext.admin import BaseView as AdminBaseView
from flask.ext.admin.actions import action
from flask.ext.admin import helpers as h
from flask.ext.security import current_user
from flask.ext.security.utils import url_for_security
from flask import redirect, flash, url_for, Response, current_app

from flask.ext.htmlbuilder import html

from quokka.modules.accounts.models import User
from quokka.core.templates import render_template
from quokka.core.widgets import PrepopulatedText
from quokka.core.admin.fields import ContentImageField
from quokka.utils.upload import dated_path, lazy_media_path
from quokka.utils import is_accessible
from quokka.utils.settings import get_setting_value
from .fields import ThumbField

from .utils import _, _l, _n


class ThemeMixin(object):
    def render(self, template, **kwargs):
        # Store self as admin_view
        kwargs['admin_view'] = self
        kwargs['admin_base_template'] = self.admin.base_template
        # Provide i18n support even if flask-babel is not installed or enabled.
        kwargs['_gettext'] = gettext
        kwargs['_ngettext'] = ngettext
        kwargs['h'] = h
        # Contribute extra arguments
        kwargs.update(self._template_args)
        theme = current_app.config.get('ADMIN_THEME', None)
        return render_template(template, theme=theme, **kwargs)


class Roled(object):

    def is_accessible(self):
        roles_accepted = getattr(self, 'roles_accepted', None)
        return is_accessible(roles_accepted=roles_accepted, user=current_user)

    def _handle_view(self, name, *args, **kwargs):
        if not current_user.is_authenticated():
            return redirect(url_for_security('login', next="/admin"))
        if not self.is_accessible():
            return self.render("admin/denied.html")


def format_datetime(self, request, obj, fieldname, *args, **kwargs):
    return html.div(style='min-width:130px;')(
        getattr(obj, fieldname).strftime(self.get_datetime_format())
    )


def view_on_site(self, request, obj, fieldname, *args, **kwargs):
    endpoint = kwargs.pop('endpoint', 'detail' if obj.published else 'preview')
    return html.a(
        href=obj.get_absolute_url(endpoint),
        target='_blank',
    )(html.i(class_="icon icon-eye-open", style="margin-right: 5px;")(),
      _l('View on site') if obj.published else _l('Preview on site'))


def format_ul(self, request, obj, fieldname, *args, **kwars):
    field = getattr(obj, fieldname)
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('ul', {}).get(fieldname, {})
    ul = html.ul(style=_args.get('style', "min-width:200px;max-width:300px;"))
    placeholder = _args.get('placeholder', u"{i}")
    lis = [html.li(placeholder.format(item=item)) for item in field]
    return ul(*lis)


def format_link(self, request, obj, fieldname, *args, **kwars):
    value = getattr(obj, fieldname)
    return html.a(href=value, title=value, target='_blank')(
        html.i(class_="icon  icon-resize-small",
               style="margin-right: 5px;")()
    )


def format_status(self, request, obj, fieldname, *args, **kwargs):
    status = getattr(obj, fieldname)
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('status', {}).get(fieldname, {})
    labels = _args.get('labels', {})
    return html.span(
        class_="label label-{0}".format(labels.get(status, 'default')),
        style=_args.get('style', 'min-height:18px;')
    )(status)


def get_url(self, request, obj, fieldname, *args, **kwargs):
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('get_url', {}).get(fieldname, {})
    attribute = _args.get('attribute', None)
    method = _args.get('method', 'get_absolute_url')
    text = getattr(obj, fieldname, '')
    if attribute:
        target = getattr(obj, attribute, None)
    else:
        target = obj

    url = getattr(target, method, lambda: '#')()

    return html.a(href=url)(text if text not in [None, 'None'] else '')


class FileAdmin(ThemeMixin, Roled, _FileAdmin):

    def __init__(self, *args, **kwargs):
        self.roles_accepted = kwargs.pop('roles_accepted', list())
        self.editable_extensions = kwargs.pop('editable_extensions', tuple())
        super(FileAdmin, self).__init__(*args, **kwargs)


class ModelAdmin(ThemeMixin, Roled, ModelView):

    form_subdocuments = {}
    datetime_format = "%Y-%m-%d %H:%M"
    formatters = {
        'datetime': format_datetime,
        'view_on_site': view_on_site,
        'ul': format_ul,
        'status': format_status,
        'get_url': get_url,
        'link': format_link
    }
    column_formatters_args = {}

    def get_datetime_format(self):
        return current_app.config.get('DATETIME_FORMAT', self.datetime_format)

    def get_instance(self, i):
        try:
            return self.model.objects.get(id=i)
        except self.model.DoesNotExist:
            flash(_("Item not found %(i)s", i=i), "error")

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


class PublishActions(object):
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


class ContentActions(object):
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
        new.last_updated_by = User.objects.get(id=current_user.id)
        new.updated_at = datetime.datetime.now()
        new.slug = "{0}-{1}".format(new.slug, random.getrandbits(32))
        new.save()
        return redirect(url_for('.edit_view', id=new.id))


class BaseIndexView(Roled, ThemeMixin, AdminIndexView):
    pass


class BaseView(Roled, ThemeMixin, AdminBaseView):
    pass


class BaseContentAdmin(ContentActions, PublishActions, ModelAdmin):
    """
    All attributes added here for example
    more info in admin source
    github.com/mrjoes/flask-admin/blob/master/flask_admin/model/base.py
    or Flask-admin documentation
    """

    roles_accepted = ('admin', 'editor', 'author')
    can_create = True
    can_edit = True
    can_delete = True

    # list_template = 'admin/model/list.html'
    # edit_template = 'admin/custom/edit.html'
    # create_template = 'admin/custom/create.html'

    column_list = (
        'title', 'slug', 'channel', 'published', 'created_at',
        'available_at', 'view_on_site'
    )

    column_formatters = {
        'view_on_site': ModelAdmin.formatters.get('view_on_site'),
        'created_at': ModelAdmin.formatters.get('datetime'),
        'available_at': ModelAdmin.formatters.get('datetime'),
        'short_url': ModelAdmin.formatters.get('link')
    }

    # column_type_formatters = {}
    # column_labels = {}
    # column_descriptions = {}
    # column_sortable_list = [] / ('name', ('user', 'user.username'))
    # column_default_sort = 'pk'
    # column_choices = {'column': ('value', 'display')}
    # column_display_pk = True

    column_filters = ['published', 'title', 'summary',
                      'created_at', 'available_at']
    column_searchable_list = ('title', 'summary')

    form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
                    'published', 'add_image', 'contents',
                    'show_on_channel', 'available_at', 'available_until',
                    'tags', 'values', 'template_type', 'license', 'authors']
    # form_excluded_columns = []
    # form = None
    # form_overrides = None

    form_widget_args = {
        'summary': {
            'style': 'width: 400px; height: 100px;'
        },
        'title': {'style': 'width: 400px'},
        'slug': {'style': 'width: 400px'},
    }

    form_args = {
        # 'body': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }

    form_subdocuments = {
        'contents': {
            'form_subdocuments': {
                None: {
                    'form_columns': ('content', 'caption', 'purpose',
                                     'order', 'thumb'),
                    'form_ajax_refs': {
                        'content': {
                            'fields': ['title', 'long_slug', 'summary']
                        }
                    },
                    'form_extra_fields': {
                        'thumb': ThumbField('thumb', endpoint="media")
                    }
                }
            }
        },
    }
    # form_extra_fields = {}
    form_extra_fields = {
        'add_image': ContentImageField(
            'Add new image',
            base_path=lazy_media_path(),
            thumbnail_size=get_setting_value('MEDIA_IMAGE_THUMB_SIZE',
                                             default=(100, 100, True)),
            endpoint="media",
            namegen=dated_path,
            permission=0o777,
            allowed_extensions="MEDIA_IMAGE_ALLOWED_EXTENSIONS",
        )
    }

    # action_disallowed_list
    # page_size = 20
    # form_ajax_refs = {
    #     'main_image': {"fields": ('title',)}
    # }

    def get_list_columns(self):
        column_list = super(BaseContentAdmin, self).get_list_columns()
        if get_setting_value('SHORTENER_ENABLED'):
            column_list += [('short_url', 'Short URL')]
        return column_list

    def after_model_change(self, form, model, is_created):
        if not hasattr(form, 'add_image'):
            return

        form.add_image.save_contents(model)
