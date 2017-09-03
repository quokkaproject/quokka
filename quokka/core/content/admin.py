# from flask_admin.helpers import get_form_data
import datetime as dt

from flask import current_app
from quokka.admin.forms import ValidationError
from quokka.admin.views import ModelView
from quokka.core.auth import get_current_user
from quokka.utils.routing import get_content_url
from quokka.utils.text import slugify

from .formats import CreateForm, get_format


class ContentView(ModelView):
    """Base form for all contents"""
    # TODO: move to base class and read from settings
    details_modal = True
    can_view_details = True
    create_modal = True
    # can_export = True
    # export_types = ['csv', 'json', 'yaml', 'html', 'xls']

    details_modal_template = 'admin/model/modals/details.html'
    # create_template = 'admin/model/create.html'

    edit_template = 'admin/quokka/edit.html'
    # TODO: ^get edit_template from content_type

    page_size = 20
    can_set_page_size = True

    form = CreateForm
    column_list = (
        'title',
        'category',
        'authors',
        'date',
        'modified',
        'language',
        'published'
    )

    column_sortable_list = (
        'title',
        'category',
        'authors',
        'date',
        'modified',
        'language',
        'published'
    )
    # column_default_sort = 'date'

    # TODO: implement scaffold_list_form in base class
    # column_editable_list = ['category', 'status', 'title']

    column_details_list = [
        'title',
        'category',
        'slug',
        'content_format',
        'content_type',
        'language',
        'date',
        'created_by',
        'modified',
        'modified_by'
    ]
    # column_export_list = []
    # column_formatters_export
    # column_formatters = {fieldname: callable} - view, context, model, name

    column_extra_row_actions = None
    """
        List of row actions (instances of :class:`~flask_admin.model.template.
        BaseListRowAction`).

        Flask-Admin will generate standard per-row actions (edit, delete, etc)
        and will append custom actions from this list right after them.

        For example::

            from flask_admin.model.template import EndpointLinkRowAction,
            LinkRowAction

            class MyModelView(BaseModelView):
                column_extra_row_actions = [
                    LinkRowAction('glyphicon glyphicon-off',
                    'http://direct.link/?id={row_id}'),
                    EndpointLinkRowAction('glyphicon glyphicon-test',
                    'my_view.index_view')
                ]
    """

    # form_edit_rules / form_create_rules
    # form_rules = [
    #     # Define field set with header text and four fields
    #     rules.FieldSet(('title', 'category', 'tags'), 'Base'),
    #     # ... and it is just shortcut for:
    #     rules.Header('Content Type'),
    #     rules.Field('summary'),
    #     rules.Field('date'),
    #     # ...
    #     # It is possible to create custom rule blocks:
    #     # MyBlock('Hello World'),
    #     # It is possible to call macros from current context
    #     # rules.Macro('my_macro', foobar='baz')
    # ]

    # def create_form(self):
    #     form = super(ContentView, self).create_form()
    #     form.content_type.choices = [('a', 'a'), ('b', 'b')]
    #     return form

    # @property
    # def extra_js(self):
    #     return [
    #         url_for('static', filename='js/quokka_admin.js')
    #     ]

    def edit_form(self, obj):
        content_format = get_format(obj)
        self.form_edit_rules = content_format.get_form_rules()
        self._refresh_form_rules_cache()
        return content_format.get_edit_form(obj)

    def get_save_return_url(self, model, is_created):
        if is_created:
            return self.get_url('.edit_view', id=model['_id'])
        return super(ContentView, self).get_save_return_url(model, is_created)

    def on_model_change(self, form, model, is_created):
        # check if already exists a record with same slug & category
        # TODO: if slug is not yet defined use title, else use slug
        existent = current_app.db.get('index', {'title': model['title'],
                                                'category': model['category']})

        if (is_created and existent) or (
                existent and existent['_id'] != model['_id']):
            raise ValidationError(f'{get_content_url(model)} already exists')

        if is_created:
            model['date'] = dt.datetime.now()
            model['created_by'] = get_current_user()
        else:
            model['modified'] = dt.datetime.now()
            model['modified_by'] = get_current_user()

        if not model.get('slug'):
            model['slug'] = slugify(model['title'])

        if not model.get('content_id'):
            model['content_id'] = current_app.db.insert(
                'contents',
                {'content': model.pop('content', None)}
            )

        model.pop('csrf_token', None)
        print(model)
        get_format(model).before_save(form, model, is_created)

    def after_model_change(self, form, model, is_created):
        get_format(model).after_save(form, model, is_created)
