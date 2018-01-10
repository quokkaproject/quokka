# from flask_admin.helpers import get_form_data
import datetime as dt
import pymongo
from flask import current_app
from quokka.admin.forms import ValidationError, rules
from quokka.admin.views import ModelView
from quokka.core.auth import get_current_user
from quokka.utils.text import slugify, slugify_category

from .formats import CreateForm, get_format
from .utils import url_for_content


class AdminContentView(ModelView):
    """Base form for all contents"""
    base_query = {}
    create_defaults = {}
    quokka_form_edit_rules = None
    quokka_form_create_rules = None

    details_modal = True
    can_view_details = True
    # create_modal = False
    # can_export = True
    # export_types = ['csv', 'json', 'yaml', 'html', 'xls']

    # details_modal_template = 'admin/model/modals/details.html'
    create_template = 'admin/quokka/create.html'
    edit_template = 'admin/quokka/edit.html'
    # EDIT template is re-taken from content_format

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
    column_default_sort = ('date', True)

    # TODO: implement scaffold_list_form in base class to enable below
    # column_editable_list = ['category', 'published', 'title']

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
        'modified_by',
        'version',
        '_isclone',
        'quokka_module',
        'quokka_format_module',
        'quokka_format_class',
        'quokka_create_form_module',
        'quokka_create_form_class',
        'category_slug',
        'authors_slug',
        'authors_string',
        'tags_slug',
        'tags_string',
        'custom_vars',
    ]

    # column_export_list = []
    # column_formatters_export
    # column_formatters = {fieldname: callable} - view, context, model, name

    # column_extra_row_actions = None
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

    # @property
    # def extra_js(self):
    #     return [
    #         url_for('static', filename='js/quokka_admin.js')
    #     ]

    def create_form(self):
        form = super(AdminContentView, self).create_form()
        if self.quokka_form_create_rules:
            self.form_create_rules = self.quokka_form_create_rules
        self._refresh_form_rules_cache()
        return form

    def edit_form(self, obj):
        content_format = get_format(obj)
        self.edit_template = content_format.get_edit_template(
            obj
        ) or self.edit_template
        if self.quokka_form_edit_rules:
            self.form_edit_rules = self.quokka_form_edit_rules
        else:
            self.form_edit_rules = content_format.get_form_edit_rules(obj)
        self._refresh_form_rules_cache()
        form = content_format.get_edit_form(obj)
        return form

    def on_form_prefill(self, form, id):
        """Fill edit form with versioned data"""
        form.content.data = current_app.db.pull_content(id)

    def get_save_return_url(self, model, is_created):
        if is_created:
            return self.get_url('.edit_view', id=model['_id'])
        return super(AdminContentView, self).get_save_return_url(model,
                                                                 is_created)

    def get_existent_record(self, form, model):
        return current_app.db.get('index', {'slug': model['slug'],
                                            'category': model['category']})

    def on_model_change(self, form, model, is_created):

        if is_created:
            # each custom module should be identified by admin and format class
            self.add_module_metadata(model)

        getattr(self, 'before_save', lambda *a, **k: None)(
            form, model, is_created
        )
        get_format(model).before_save(form, model, is_created)

        if not model.get('slug'):
            model['slug'] = slugify(model['title'])

        if not model.get('category'):
            # When category is hidden on form it should be ''
            model['category'] = ''

        existent = self.get_existent_record(form, model)

        if (is_created and existent) or (
                existent and existent['_id'] != model['_id']):
            raise ValidationError(
                f'{url_for_content(model, include_ext=False)} already exists'
            )

        now = dt.datetime.now()
        current_user = get_current_user()

        if is_created:
            # this defaults are also applied for cloning action

            # SIGNATURE
            model['_id'] = current_app.db.generate_id()
            model['date'] = now
            model['created_by'] = current_user
            model['published'] = False
            model['modified'] = None
            model['modified_by'] = None

            # DEFAULTS
            default_locale = current_app.config.get(
                'BABEL_DEFAULT_LOCALE', 'en'
            )
            model['language'] = self.base_query.get('language', default_locale)
            model['content_type'] = self.base_query.get(
                'content_type', 'article'
            )

        defaults_attr = f"{'create' if is_created else 'edit'}_defaults"
        for key, val in getattr(self, defaults_attr, {}).items():
            model.setdefault(key, val)

        model['modified'] = now
        model['modified_by'] = current_user

        model.pop('csrf_token', None)

        self.slugify_search_data(model)
        current_app.db.push_content(model)

    def slugify_search_data(self, model):
        fields = ['category', 'authors', 'tags']
        for field in fields:
            _slugify = slugify_category if field == 'category' else slugify
            data = model.get(field)
            if data and isinstance(data, list):
                slugified = [_slugify(item) for item in data]
                model[f'{field}_slug'] = slugified
                # tinymongo has limitation to search in list fields
                # https://github.com/schapman1974/tinymongo/issues/42
                # while the above is not fixed this workaround is needed
                # app.db.index.find({'tags_string': {'$regex': '.*,tag,.*'}})
                model[f'{field}_string'] = f',{",".join(slugified)},'
            elif data and isinstance(data, str):
                model[f'{field}_slug'] = _slugify(data)
            else:
                model[f'{field}_slug'] = data

    def after_model_change(self, form, model, is_created):
        # call admin custom hook
        getattr(self, 'after_save', lambda *a, **k: None)(
            form, model, is_created
        )
        # call the method from format
        get_format(model).after_save(form, model, is_created)

    def add_module_metadata(self, model):
        quokka_format = get_format(model)
        form = getattr(self.__class__, 'form', self.get_form())
        model['quokka_module'] = self.__module__
        model['quokka_format_module'] = quokka_format.__module__
        model['quokka_format_class'] = quokka_format.__class__.__name__
        model['quokka_create_form_module'] = form.__module__
        model['quokka_create_form_class'] = form.__class__.__name__

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        """
            Get list of objects from TinyDB
            :param page:
                Page number
            :param sort_column:
                Sort column
            :param sort_desc:
                Sort descending
            :param search:
                Search criteria
            :param filters:
                List of applied fiters
            :param execute:
                Run query immediately or not
            :param page_size:
                Number of results. Defaults to ModelView's page_size. Can be
                overriden to change the page_size limit. Removing the page_size
                limit requires setting page_size to 0 or False.
        """
        query = {**self.base_query}

        # Filters
        if self._filters:
            data = []

            for flt, _, value in filters:
                f = self._filters[flt]
                data = f.apply(data, f.clean(value))

            if data:
                if len(data) == 1:
                    query = data[0]
                else:
                    query['$and'] = data

        # Search
        if self._search_supported and search:
            query = self._search(query, search)

        # Get count
        count = self.coll.find(
            query).count() if not self.simple_list_pager else None

        # Sorting
        sort_by = None

        if sort_column:
            sort_by = [(sort_column, pymongo.DESCENDING
                        if sort_desc else pymongo.ASCENDING)]
        else:
            order = self._get_default_order()

            if order:
                sort_by = [(order[0], pymongo.DESCENDING
                            if order[1] else pymongo.ASCENDING)]

        # Pagination
        if page_size is None:
            page_size = self.page_size

        skip = 0

        if page and page_size:
            skip = page * page_size

        results = self.coll.find(
            query, sort=sort_by, skip=skip, limit=page_size)

        if execute:
            results = list(results)

        return count, results

    def get_one(self, id):
        """
            Return single model instance by ID
            :param id:
                Model ID
        """
        query = {**self.base_query}
        query['_id'] = self._get_valid_id(id)
        return self.coll.find_one(query)


class AdminArticlesView(AdminContentView):
    """Only articles"""
    base_query = {'content_type': 'article'}
    create_defaults = {'comments': True}


class AdminPagesView(AdminContentView):
    """Only pages"""
    base_query = {'content_type': 'page'}
    create_defaults = {'comments': False}
    quokka_form_create_rules = [
        rules.FieldSet(('title', 'summary')),
        rules.FieldSet(('content_format',)),
        rules.csrf_token
    ]
    quokka_form_edit_rules = [
        rules.FieldSet(('title', 'summary')),
        rules.Field('content'),
        # rules.FieldSet(('category', 'authors', 'tags')),
        rules.FieldSet(('date',)),
        rules.FieldSet(('slug',)),
        rules.Field('published'),
        rules.Field('comments'),
        rules.Field('custom_vars'),
        rules.csrf_token
    ]


class AdminBlocksView(AdminContentView):
    """Only blocks"""
    base_query = {'content_type': 'block'}
    create_defaults = {'comments': False}
    column_list = (
        'title',
        'date',
        'modified',
        'language',
        'published'
    )
    column_sortable_list = (
        'title',
        'date',
        'modified',
        'language',
        'published'
    )
    quokka_form_create_rules = [
        rules.FieldSet(('title', 'summary')),
        rules.FieldSet(('content_format',)),
        rules.csrf_token
    ]
    quokka_form_edit_rules = [
        rules.FieldSet(('title', 'summary')),
        rules.Field('content'),
        # rules.FieldSet(('category', 'authors', 'tags')),
        rules.FieldSet(('date',)),
        rules.FieldSet(('slug',)),
        rules.Field('published'),
        rules.Field('comments'),
        rules.Field('block_items'),
        rules.Field('custom_vars'),
        rules.csrf_token
    ]

    def get_existent_record(self, form, model):
        return current_app.db.get(
            'index',
            {'slug': model['slug'],
             'category': model['category'],
             'content_type': 'block'}
        )

    def before_save(self, form, model, is_created):
        if 'block_items' in model:
            model['block_items'].sort(key=lambda x: x['order'])
            for i, item in enumerate(model['block_items']):

                item.pop('csrf_token', None)
                item['order'] = i

                for ref in ['author', 'category', 'tag', 'url']:
                    if item['item'].startswith(f"{ref}::"):
                        item[f"{ref}_id"] = item['item'].split('::')[-1]
                    else:
                        item[f"{ref}_id"] = None

                content_types = ('article::', 'page::', 'block::')
                if item['item'].startswith(content_types):
                    full_slug = item['item'].split('::')[-1]
                    slug = full_slug.split('/')[-1]
                    category = full_slug.rpartition('/')[0]
                    args = {'slug': slug}
                    if category:
                        args['category'] = category

                    content = current_app.db.get('index', args)
                    if content:
                        item['index_id'] = content['_id']
                else:
                    item['index_id'] = None
