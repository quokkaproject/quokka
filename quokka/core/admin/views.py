# Create customized index view class

from flask import current_app
from quokka.core.models import Content
from quokka.utils.routing import expose

from .ajax import AjaxModelLoader
from .models import BaseIndexView, BaseView, ModelAdmin


class IndexView(BaseIndexView):
    roles_accepted = ('admin', 'editor', 'moderator', 'writer', 'staff')

    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class InspectorView(BaseView):
    roles_accepted = ('admin',)

    @expose('/')
    def index(self):
        context = {
            "app": current_app
        }
        return self.render('admin/inspector.html', **context)


###############################################################
# Admin model views
###############################################################

class LinkAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'writer', 'moderator')
    column_list = ('title', 'channel', 'slug', 'published')
    form_columns = ('title', 'slug', 'channel', 'link', 'contents',
                    'values', 'available_at', 'available_until', 'published')


class ConfigAdmin(ModelAdmin):
    roles_accepted = ('admin', 'developer')
    column_list = ("group", "description", "published",
                   "created_at", "updated_at")
    column_filters = ("group", "description")
    form_columns = ("group", "description", "published", "values")


class SubContentPurposeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')


class ChannelTypeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')


class ContentTemplateTypeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')


class ChannelAdmin(ModelAdmin):
    edit_template = 'admin/custom/edit.html'
    create_template = 'admin/custom/create.html'
    roles_accepted = ('admin', 'editor')
    column_list = ('title', 'long_slug', 'is_homepage',
                   'channel_type', 'created_at', 'available_at', 'published')
    column_filters = ['published', 'is_homepage', 'include_in_rss',
                      'show_in_menu', 'indexable']
    column_searchable_list = ('title', 'description')
    form_columns = ['title', 'slug', 'description', 'parent', 'is_homepage',
                    'include_in_rss', 'indexable', 'show_in_menu', 'order',
                    'published', 'canonical_url', 'values', 'channel_type',
                    'inherit_parent', 'content_filters', 'available_at',
                    'available_until', 'render_content']
    column_formatters = {'created_at': ModelAdmin.formatters.get('datetime'),
                         'available_at': ModelAdmin.formatters.get('datetime')}
    form_subdocuments = {}

    form_widget_args = {
        'description': {
            'rows': 20,
            'cols': 20,
            'class': 'text_editor',
            'style': "margin: 0px; width: 400px; height: 250px;"
        },
        'title': {'style': 'width: 400px'},
        'slug': {'style': 'width: 400px'},
    }

    form_ajax_refs = {
        'render_content': AjaxModelLoader('render_content',
                                          Content,
                                          fields=['title', 'slug']),
        'parent': {'fields': ['title', 'slug', 'long_slug']},
    }
