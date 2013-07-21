# coding : utf -8
from quokka import admin
from quokka.core.admin.models import ModelAdmin

from .models import Post


class PostAdmin(ModelAdmin):
    """
    All attributes added here for example
    more info in admin source
    github.com/mrjoes/flask-admin/blob/master/flask_admin/model/base.py
    or Flask-admin documentation
    """

    roles_accepted = ('admin', 'editor')
    can_create = True
    can_edit = True
    can_delete = True

    # list_template = 'admin/model/list.html'
    edit_template = 'admin/custom/edit.html'
    create_template = 'admin/custom/create.html'

    column_list = ('title', 'slug', 'channel', 'published')
    # column_exclude_list = []

    # column_formatters = {}
    # column_type_formatters = {}
    # column_labels = {}
    # column_descriptions = {}
    # column_sortable_list = [] / ('name', ('user', 'user.username'))
    # column_default_sort = 'pk'
    # column_choices = {'column': ('value', 'display')}
    #  column_display_pk = True
    column_filters = ['published']
    column_searchable_list = ('title', 'body', 'summary')

    form_columns = ['title', 'slug', 'channel', 'channels', 'summary', 'body',
                    'published', 'comments']
    # form_excluded_columns = []
    # form = None
    # form_overrides = None

    form_widget_args = {
        'body': {
            'rows': 20,
            'cols': 20,
            'class': 'html_editor',
            'style': "margin: 0px; width: 725px; height: 360px;"
        },
        'summary': {
            'style': 'width: 400px; height: 100px;'
        },
        'title': {'style': 'width: 400px'},
        'slug': {'style': 'width: 400px'},
    }

    # form_args = {
    #     'body': {
    #         'widget': BigTextArea()
    #     }
    # }

    # form_extra_fields = {}

    # action_disallowed_list

    # page_size = 20


admin.add_view(PostAdmin(Post, category='Content'))
