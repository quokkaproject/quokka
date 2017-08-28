# coding: utf -8

from flask import current_app, redirect
# from flask_admin.babel import gettext, ngettext
from flask_admin import AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin as _FileAdmin
from flask_admin.contrib.pymongo import ModelView as PyMongoModelView
# from flask_admin import helpers as h
from flask_login import current_user, login_url
from quokka.admin.actions import CloneAction, PublishAction
# from quokka.template import render_template
# from quokka.admin.widgets import PrepopulatedText
# from quokka.admin.fields import ContentImageField
# from quokka.utils.upload import dated_path, lazy_media_path
from quokka.utils.routing import expose


# from flask_admin import BaseView as AdminBaseView

# from quokka.admin.fields import ThumbField

# from quokka.admin import formatters


class ThemeMixin(object):
    pass
    # def render(self, template, **kwargs):
    #     # Store self as admin_view
    #     kwargs['admin_view'] = self
    #     kwargs['admin_base_template'] = self.admin.base_template
    #     # Provide i18n support even if flask-babel is not installed or enabled.
    #     kwargs['_gettext'] = gettext
    #     kwargs['_ngettext'] = ngettext
    #     kwargs['h'] = h
    #     # Contribute extra arguments
    #     kwargs.update(self._template_args)
    #     theme = current_app.config.get('ADMIN_THEME')
    #     return render_template(template, theme=theme, **kwargs)

    # def render(self, template, **kwargs):
    #     """
    #         Render template
    #         :param template:
    #             Template path to render
    #         :param kwargs:
    #             Template arguments
    #     """
    #     # Store self as admin_view
    #     kwargs['admin_view'] = self
    #     kwargs['admin_base_template'] = self.admin.base_template

    #     # Provide i18n support even if flask-babel is not installed
    #     # or enabled.
    #     kwargs['_gettext'] = babel.gettext
    #     kwargs['_ngettext'] = babel.ngettext
    #     kwargs['h'] = h

    #     # Expose get_url helper
    #     kwargs['get_url'] = self.get_url

    #     # Expose config info
    #     kwargs['config'] = current_app.config

    #     # Contribute extra arguments
    #     kwargs.update(self._template_args)

    #     return render_template(template, **kwargs)


class RequiresLogin(object):

    def _handle_view(self, *args, **kwargs):  # noqa
        """Admin views requires login"""
        if current_app.config.get('ADMIN_REQUIRES_LOGIN') is True:
            if not current_user.is_authenticated:
                return redirect(login_url('quokka.login', next_url="/admin"))


class FileAdmin(ThemeMixin, RequiresLogin, _FileAdmin):

    def __init__(self, *args, **kwargs):
        self.editable_extensions = kwargs.pop('editable_extensions', tuple())
        super(FileAdmin, self).__init__(*args, **kwargs)


class IndexView(RequiresLogin, ThemeMixin, AdminIndexView):

    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class ModelView(CloneAction, PublishAction,
                ThemeMixin, RequiresLogin,
                PyMongoModelView):
    """Base model view for all contents"""

    page_size = 20
    can_set_page_size = True

    # form_subdocuments = {}
    # datetime_format = "%Y-%m-%d %H:%M"
    # formatters = {
    #     'datetime': formatters.format_datetime,
    #     'view_on_site': formatters.view_on_site,
    #     'ul': formatters.format_ul,
    #     'status': formatters.format_status,
    #     'get_url': formatters.get_url,
    #     'link': formatters.format_link
    # }
    # column_formatters_args = {}

    # def get_datetime_format(self):
    #     return current_app.config.get('DATETIME_FORMAT', self.datetime_format)


# class BaseContentView(ModelView):
#     """
#     All attributes added here for example
#     more info in admin source
#     github.com/mrjoes/flask-admin/blob/master/flask_admin/model/base.py
#     or Flask-admin documentation
#     """

#     roles_accepted = ('admin', 'editor', 'author')
#     can_create = True
#     can_edit = True
#     can_delete = True

#     # list_template = 'admin/model/list.html'
#     # edit_template = 'admin/custom/edit.html'
#     # create_template = 'admin/custom/create.html'

#     column_list = (
#         'title', 'slug', 'channel', 'published', 'created_at',
#         'available_at', 'view_on_site'
#     )

#     column_formatters = {
#         'view_on_site': formatters.view_on_site,
#         'created_at': formatters.format_datetime,
#         'available_at': formatters.format_datetime
#     }

#     # column_type_formatters = {}
#     # column_labels = {}
#     # column_descriptions = {}
#     # column_sortable_list = [] / ('name', ('user', 'user.username'))
#     # column_default_sort = 'pk'
#     # column_choices = {'column': ('value', 'display')}
#     # column_display_pk = True

#     column_filters = ['published', 'title', 'summary',
#                       'created_at', 'available_at']
#     column_searchable_list = ('title', 'summary')

#     form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
#                     'published', 'add_image', 'contents',
#                     'show_on_channel', 'available_at', 'available_until',
#                     'tags', 'values', 'template_type', 'license', 'authors']
#     # form_excluded_columns = []
#     # form = None
#     # form_overrides = None

#     form_widget_args = {
#         'summary': {
#             'style': 'width: 400px; height: 100px;'
#         },
#         'title': {'style': 'width: 400px'},
#         'slug': {'style': 'width: 400px'},
#     }

#     form_args = {
#         # 'body': {'widget': TextEditor()},
#         'slug': {'widget': PrepopulatedText(master='title')}
#     }

#     form_subdocuments = {
#         'contents': {
#             'form_subdocuments': {
#                 None: {
#                     'form_columns': ('content', 'caption', 'purpose',
#                                      'order', 'thumb'),
#                     'form_ajax_refs': {
#                         'content': {
#                             'fields': ['title', 'long_slug', 'summary']
#                         }
#                     },
#                     'form_extra_fields': {
#                         'thumb': ThumbField('thumb', endpoint="media")
#                     }
#                 }
#             }
#         },
#     }
#     # form_extra_fields = {}
#     form_extra_fields = {
#         'add_image': ContentImageField(
#             'Add new image',
#             base_path=lazy_media_path(),
#             # thumbnail_size=get_setting_value('MEDIA_IMAGE_THUMB_SIZE',
#             #                                  default=(100, 100, True)),
#             endpoint="media",
#             namegen=dated_path,
#             permission=0o777,
#             allowed_extensions="MEDIA_IMAGE_ALLOWED_EXTENSIONS",
#         )
#     }

#     # action_disallowed_list
#     # page_size = 20
#     # form_ajax_refs = {
#     #     'main_image': {"fields": ('title',)}
#     # }

#     # def get_list_columns(self):
#     #     column_list = super(BaseContentAdmin, self).get_list_columns()
#     #     if get_setting_value('SHORTENER_ENABLED'):
#     #         column_list += [('short_url', 'Short URL')]
#     #     return column_list

#     def after_model_change(self, form, model, is_created):
#         if not hasattr(form, 'add_image'):
#             return

#         form.add_image.save_contents(model)
