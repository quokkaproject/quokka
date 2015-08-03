# Create customized index view class

from flask import current_app, flash
from flask.ext.admin.actions import action
from quokka.core.models import Content
from quokka.utils.routing import expose
from quokka.core.widgets import TextEditor, PrepopulatedText
from .utils import _, _l
from .ajax import AjaxModelLoader
from .models import (
    BaseIndexView,
    BaseView,
    ModelAdmin,
    BaseContentAdmin,
    ContentActions,
    PublishActions
)


class IndexView(BaseIndexView):
    roles_accepted = ('admin', 'editor', 'moderator', 'writer', 'staff',
                      'author')

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

class LinkAdmin(BaseContentAdmin):
    roles_accepted = ('admin', 'editor', 'writer', 'moderator', 'author')
    column_list = ('title', 'channel', 'slug', 'force_redirect', 'published')
    form_columns = ('title', 'slug', 'channel',
                    'related_channels',
                    'link', 'show_on_channel',
                    'force_redirect', 'increment_visits', 'visits',
                    'content_format', 'summary', 'add_image', 'contents',
                    'values', 'tags', 'available_at',
                    'available_until', 'published')

    form_args = {
        'summary': {'widget': TextEditor()}
    }


class ConfigAdmin(PublishActions, ModelAdmin):
    roles_accepted = ('admin', 'developer')
    column_list = ("group", "description", "published",
                   "created_at", "updated_at")
    column_filters = ("group", "description")
    form_columns = ("group", "description", "published", "values")


class SubContentPurposeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'author')


class ChannelTypeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'author')


class ContentTemplateTypeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'author')


class ChannelAdmin(ContentActions, PublishActions, ModelAdmin):
    roles_accepted = ('admin', 'editor', 'author')
    column_list = ('title', 'long_slug', 'is_homepage',
                   'channel_type', 'created_at', 'available_at', 'published',
                   'view_on_site')
    column_filters = ['published', 'is_homepage', 'include_in_rss',
                      'show_in_menu', 'indexable']
    column_searchable_list = ('title', 'description')
    form_columns = ['title', 'slug', 'content_format', 'description',
                    'parent', 'is_homepage', 'roles',
                    'include_in_rss', 'indexable', 'show_in_menu', 'order',
                    'per_page', 'tags', 'sort_by',
                    'published', 'canonical_url', 'values', 'channel_type',
                    'inherit_parent', 'content_filters', 'available_at',
                    'available_until', 'render_content', 'redirect_url']
    column_formatters = {
        'view_on_site': ModelAdmin.formatters.get('view_on_site'),
        'created_at': ModelAdmin.formatters.get('datetime'),
        'available_at': ModelAdmin.formatters.get('datetime')
    }
    form_subdocuments = {}

    form_widget_args = {
        'title': {'style': 'width: 400px'},
        'slug': {'style': 'width: 400px'},
    }

    form_args = {
        'description': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }

    form_ajax_refs = {
        'render_content': AjaxModelLoader('render_content',
                                          Content,
                                          fields=['title', 'slug']),
        'parent': {'fields': ['title', 'slug', 'long_slug']},
    }

    @action(
        'set_homepage',
        _l('Set as homepage'),
        _l('Set as homepage?')
    )
    def action_set_homepage(self, ids):
        if len(ids) > 1:
            flash(
                _("You can select only one item for this action"),
                'error'
            )
            return

        instance = self.get_instance(ids[0])
        if instance.is_homepage:
            flash(
                _("Already homepage"),
                'error'
            )
            return

        current_homepage = self.model.objects.filter(is_homepage=True)
        try:
            current_homepage.update(is_homepage=False)
            instance.is_homepage = True
            instance.save()
        except Exception as e:
            current_homepage.update(is_homepage=True)
            flash(_('Error setting channel as homepage %s', e), 'error')
        else:
            flash(_('Channel set as homepage'))
