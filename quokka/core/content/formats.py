import datetime as dt
import getpass
import json
from .parsers import markdown
from flask import current_app as app, Markup
from flask_admin.helpers import get_form_data
from flask_admin.model.fields import InlineFieldList, InlineFormField
from quokka.admin.forms import Form, fields, rules, validators
from werkzeug.utils import import_string


# Utils


def get_content_formats(instances=False):
    content_formats = app.config.get(
        'CONTENT_FORMATS',
        {
            'markdown': {
                'choice_text': 'Markdown',
                'help_text': 'Markdown text editor',
                'content_format_class':
                    'quokka.core.content.formats.MarkdownFormat'
            }
        }
    )
    if instances:
        for _, data in content_formats:
            data['content_format_instance'] = import_string(
                data['content_format_class']
            )()
    return content_formats


def get_content_format_choices():
    content_formats = get_content_formats()
    return [
        # ('value', 'TEXT')
        (identifier, data['choice_text'])
        for identifier, data
        in content_formats.items()
    ]


def get_format(obj):
    content_formats = get_content_formats()
    try:
        obj_content_format = content_formats[obj['content_format']]
        content_format = import_string(
            obj_content_format['content_format_class']
        )()
        return content_format
    except (KeyError):
        return PlainFormat()


def get_edit_form(obj):
    return get_format(obj).get_edit_form(obj)


def validate_category(form, field):
    denied_categories = app.config.get(
        'DENIED_CATEGORIES',
        ['tag', 'tags', 'categories', 'author', 'authors', 'user',
         'index', 'feed', 'admin', 'adm', 'login', 'logout', 'sitemap',
         'block']
    )
    if field.data is not None:
        items = field.data.split(',')
        if len(items) > 1:
            return 'You can select only one category'
        for item in items:
            root_name = item.split('/')[0]
            if root_name in denied_categories or root_name.startswith('@'):
                return f'You cannot use `{root_name}` as a category start name'


def get_category_kw(field):
    categories = list(app.db.category_set(sort=False))
    categories.extend(app.config.get('CATEGORIES', []))
    categories = sorted(list(set(categories)))
    return {'data-tags': json.dumps(categories),
            'data-placeholder': 'One category or leave blank'}


def validate_block_item(form, field):
    if field.data is not None:
        items = field.data.split(',')
        if len(items) > 1:
            return 'You can select only one URL for each item'


def get_block_item_kw(field):
    items = [
        f"{d['content_type']}::{d['title']}::{d['category']}/{d['slug']}"
        for d in app.db.content_set()
        if d['title'] not in app.theme_context.get('TEXTBLOCKS', [])
    ]
    index = app.theme_context.get('INDEX_CATEGORY')
    items.append(f"category::{index}")
    items.extend([
        f"category::{category}"
        for category in app.db.category_set() if category
    ])
    items.extend([
        f"tag::{tag}" for tag in app.db.tag_set()
    ])
    items.extend([
        f"author::{author}" for author in app.db.author_set()
    ])
    items.extend([
        f"url::{item[0]}::{item[1]}"
        for item in app.config.get('INTERNAL_URLS', [])
    ])
    items.extend([
        f"url::category_feed_{category}::{category}/index.{ext}"
        for ext in ['rss', 'atom']
        for category in app.db.category_set() if category
    ])
    items.extend([
        f"url::tag_feed_{tag}::{tag}/index.{ext}"
        for ext in ['rss', 'atom']
        for tag in app.db.tag_set()
    ])
    block_items = sorted(list(set(items)))
    return {'data-tags': json.dumps(block_items),
            'data-placeholder': 'Start typing, select existing or add new URL'}


def get_default_category():
    return app.config.get('DEFAULT_CATEGORY')


def get_authors_kw(field):
    authors = app.db.author_set(sort=False)
    authors.extend(app.config.get('AUTHORS', []))
    authors.append(getpass.getuser())
    authors = sorted(list(set(authors)))
    return {'data-tags': json.dumps(authors),
            'data-placeholder':
                'Enter one or more comma separated author names'}


def get_default_author():
    authors = app.config.get('AUTHORS')
    return authors[0] if authors else getpass.getuser()


def get_tags_kw(field):
    tags = app.db.tag_set(sort=False)
    tags.extend(app.config.get('TAGS', []))
    tags = sorted(list(set(tags)))
    return {'data-tags': json.dumps(tags),
            'data-placeholder': 'Comma separated tags'}


def get_default_language():
    return app.config.get('BABEL_DEFAULT_LOCALE', 'en')

# classes


class BaseForm(Form):

    title = fields.StringField(
        'Title', [validators.required()],
        description='TIP: `My Title` turns to`my-title.html` url'
    )
    summary = fields.TextAreaField('Summary')
    category = fields.Select2TagsField(
        'Category',
        [validators.CallableValidator(validate_category)],
        save_as_list=False,
        render_kw=get_category_kw,
        default=get_default_category,
        description=(
            'TIP: Leave blank and url will be `/my-title.html`<br>'
            '`foo` url will be `/foo/my-title.html` <br>'
            '`foo/bar` url will be `/foo/bar/my-title.html` <br>'
        )
    )
    authors = fields.Select2TagsField(
        'Authors',
        [validators.required()],
        save_as_list=True,
        render_kw=get_authors_kw,
        default=get_default_author
    )


class CreateForm(BaseForm):
    """Default create form where content format is chosen"""
    # TODO: Make content_type an optional field by ASK_CONTENT_TYPE config
    # content_type = fields.SelectField(
    #     'Type',
    #     [validators.required()],
    #     choices=[('article', 'Article'), ('page', 'Page')]
    # )
    content_format = fields.SmartSelect2Field(
        'Format',
        [validators.required()],
        choices=get_content_format_choices,
        # TODO: remove this `allow_blank` once select2 submit on enter is fix
        allow_blank=True
    )


class CustomVariablesForm(Form):
    key = fields.StringField(
        'Key', [validators.required()],
        description='lower_snake_case'
    )
    value = fields.StringField(
        'Value', [validators.required()],
        description=(
            'Optionally define format using @int,@float,@bool,@json '
            'ex:`@float 42.1` or `@int 42` or `@bool false` '
            'or `@json ["item1", "item2"]`'
        )
    )


class BlockItemForm(Form):
    item = fields.Select2TagsField(
        'Item',
        [validators.required(),
         validators.CallableValidator(validate_block_item)],
        save_as_list=False,
        render_kw=get_block_item_kw,
        description=(
            'Enter absolute URL `http://..` or `/foo/bar.html` '
            'or select existing content.'
        )
    )
    name = fields.StringField('Name', description='optional')
    order = fields.IntegerField('Order', default=0)
    item_type = fields.SmartSelect2Field(
        'Type',
        [validators.required()],
        default='link',
        choices=lambda: [
            item for item in
            app.config.get('BLOCK_ITEM_TYPES', [('link', 'Link')])
        ]
    )

    custom_vars = InlineFieldList(
        InlineFormField(CustomVariablesForm), label='Custom Variables'
    )

    index_id = fields.HiddenField('index_id')
    category_id = fields.HiddenField('category_id')
    tag_id = fields.HiddenField('tag_id')
    author_id = fields.HiddenField('author_id')
    url_id = fields.HiddenField('url_id')
    content_type = fields.HiddenField('content_type', default='block_item')


class BaseEditForm(BaseForm):
    """Edit form with all missing fields except `content`"""

    # content_type = fields.PassiveStringField(
    #     'Type',
    #     render_kw=READ_ONLY
    # )
    # content_format = fields.PassiveStringField(
    #     'Format',
    #     render_kw=READ_ONLY
    # )

    tags = fields.Select2TagsField(
        'Tags',
        save_as_list=True,
        render_kw=get_tags_kw
    )
    date = fields.DateTimeField(
        'Date',
        [validators.required()],
        default=dt.datetime.now
    )
    modified = fields.HiddenField('Modified')
    slug = fields.StringField('Slug')
    language = fields.SmartSelect2Field(
        'Language',
        choices=lambda: [
            (lng, lng)
            for lng in app.config.get('BABEL_LANGUAGES', ['en'])
        ],
        default=get_default_language
    )
    # translations = fields.HiddenField('Translations')
    # todo: ^ create action 'add translation'
    published = fields.BooleanField(
        'Status',
        render_kw={
            'data-toggle': "toggle",
            'data-on': "Published",
            'data-off': "Draft",
            "data-onstyle": 'success'
        }
    )
    comments = fields.BooleanField(
        'Comments',
        default=True,
        render_kw={
            'data-toggle': "toggle",
            'data-on': "Enabled",
            'data-off': "Disabled",
            "data-onstyle": 'success'
        }
    )

    # to be used only for Block type
    block_items = InlineFieldList(
        InlineFormField(BlockItemForm), label='Items'
    )

    custom_vars = InlineFieldList(
        InlineFormField(CustomVariablesForm), label='Custom Variables'
    )


class BaseFormat(object):
    identifier = None
    edit_form = BaseEditForm
    form_edit_rules = [
        rules.FieldSet(('title', 'summary')),
        rules.Field('content'),
        rules.FieldSet(('category', 'authors', 'tags')),
        rules.FieldSet(('date',)),
        rules.FieldSet(('slug',)),
        rules.Field('published'),
        rules.Field('comments'),
        rules.Field('custom_vars'),
        rules.csrf_token
    ]

    def get_edit_form(self, obj):
        return self.edit_form(get_form_data(), **obj)

    def get_edit_template(self, obj):
        return 'admin/quokka/edit.html'

    def get_identifier(self):
        return self.identifier or self.__class__.__name__

    def get_form_edit_rules(self, obj):
        return self.form_edit_rules

    def before_save(self, form, model, is_created):
        """optional"""

    def after_save(self, form, model, is_created):
        """optional"""

    def extra_js(self):
        return []

    def render_content(self, obj):

        if not isinstance(obj, dict):
            content = obj.data
        else:
            content = obj

        if 'content' not in content:
            content = app.db.get_with_content(_id=content['_id'])

        return content['content']

    def render(self, obj):
        # TODO: PRE-RENDER
        rv = self.render_content(obj)
        # TODO: POST-RENDER
        return rv


# Customs


class PlainEditForm(BaseEditForm):
    content = fields.TextAreaField('Plain Content')


class PlainFormat(BaseFormat):
    edit_form = PlainEditForm


class HTMLEditForm(BaseEditForm):
    content = fields.TextAreaField('HTML Content')


class HTMLFormat(BaseFormat):
    edit_form = HTMLEditForm


class MarkdownEditForm(BaseEditForm):
    content = fields.TextAreaField('Markdown Content')


class MarkdownFormat(BaseFormat):
    edit_form = MarkdownEditForm

    def render_content(self, obj):
        content = super().render_content(obj)
        if content:
            return Markup(markdown(content))
        return content or ''
