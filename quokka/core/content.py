# coding: utf-8

# from flask_admin.helpers import get_form_data
from quokka.admin.utils import _
from quokka.admin.views import ModelView
from quokka.db import collection_index
from quokka.core.content_types import CreateForm, get_edit_form


class ContentView(ModelView):
    """Base form for all contents"""
    # TODO: move to base class and read from settings
    details_modal = True
    can_view_details = True
    create_modal = True
    can_export = True
    export_types = ['csv', 'json', 'yaml', 'html', 'xls']
    details_modal_template = 'admin/model/modals/details.html'
    page_size = 20
    can_set_page_size = True

    form = CreateForm
    column_list = (
        'title',
        'category',
        'authors',
        'date',
        'modified',
        'lang',
        'status'
    )

    column_sortable_list = (
        'title',
        'category',
        'authors',
        'date',
        'modified',
        'lang',
        'status'
    )
    # column_default_sort = 'date'

    # TODO: implement scaffold_list_form in base class
    # column_editable_list = ['category', 'status', 'title']

    column_details_list = ['content_type']
    # column_export_list = []
    # column_formatters_export
    # column_formatters = {fieldname: callable} - view, context, model, name

    column_extra_row_actions = None
    """
        List of row actions (instances of :class:`~flask_admin.model.template.BaseListRowAction`).

        Flask-Admin will generate standard per-row actions (edit, delete, etc)
        and will append custom actions from this list right after them.

        For example::

            from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction

            class MyModelView(BaseModelView):
                column_extra_row_actions = [
                    LinkRowAction('glyphicon glyphicon-off', 'http://direct.link/?id={row_id}'),
                    EndpointLinkRowAction('glyphicon glyphicon-test', 'my_view.index_view')
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

    def edit_form(self, obj):
        # form = EditContentForm(get_form_data(), **obj)
        # return form
        return get_edit_form(obj)


def configure(app, db, admin):
    admin.register(
        collection_index,
        ContentView,
        name=_('Content'),
        endpoint='contentview'
    )
    return 'content'
