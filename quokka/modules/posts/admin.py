# coding : utf -8
from quokka import admin
from wtforms.widgets import TextArea
from flask.ext.superadmin.model.backends.mongoengine import ModelAdmin
from quokka.core.admin.models import Roled

from .models import Post


class BigTextArea(TextArea):
    def __init__(self, *args, **kwargs):
        super(BigTextArea, self).__init__()
        self.rows = kwargs.get('rows')
        self.cols = kwargs.get('cols')
        self.css_cls = kwargs.get('css_cls')
        self.style_ = kwargs.get('style_')

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (self.css_cls, c)
        kwargs['rows'] = self.rows
        kwargs['cols'] = self.cols
        kwargs['style'] = self.style_
        return super(BigTextArea, self).__call__(field, **kwargs)


class PostAdmin(Roled, ModelAdmin):
    roles_accepted = ('admin', 'editor')
    list_display = ('title', 'slug', 'channel', 'published')
    list_per_page = 20
    exclude = ['created_at', 'created_by', 'updated_at', 'last_updated_by']
    only = None
    fields = None
    readonly_fields = []
    fields_order = ['title', 'slug', 'channel', 'channels',
                    'body', 'published', 'comments']
    form = None
    can_edit = True
    can_create = True
    can_delete = True
    list_template = 'admin/model/list.html'
    edit_template = 'admin/model/edit.html'
    add_template = 'admin/model/add.html'
    delete_template = 'admin/model/delete.html'
    search_fields = ['title', 'body']
    actions = None
    field_overrides = {'channels': {'label': 'Extra Channels', 'description': 'Optional'}}
    # a dictionary of field_name: overridden_params_dict, e.g.
    # { 'first_name': { 'label': 'First', 'description': 'This is first name' } }
    # parameters that can be overridden: label, description, validators, filters, default
    field_args = {'body': {'widget': BigTextArea(rows=20, cols=20, css_cls="html_editor", style_="margin: 0px; width: 725px; height: 360px;")}}


admin.register(Post, PostAdmin, category="content")
