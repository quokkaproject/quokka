import datetime as dt
import getpass
import json

from flask import current_app
from flask_admin.helpers import get_form_data
from quokka.admin.forms import READ_ONLY, Form, fields, rules, validators
from werkzeug.utils import import_string

# Utils


def get_content_formats(instances=False):
    content_formats = current_app.config.get(
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
        for identifier, data in content_formats:
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
    if field.data is not None:
        items = field.data.split(',')
        if len(items) > 1:
            return 'You can select only one category'


def get_category_kw(field):
    categories = current_app.db.value_set('index', 'category', sort=False)
    categories.extend(current_app.config.get('CATEGORIES', []))
    categories = sorted(list(set(categories)))
    return {'data-tags': json.dumps(categories)}


def get_default_category():
    return current_app.config.get('DEFAULT_CATEGORY')


def get_authors_kw(field):
    authors = current_app.db.author_set(sort=False)
    authors.extend(current_app.config.get('AUTHORS', []))
    authors.append(getpass.getuser())
    authors = sorted(list(set(authors)))
    return {'data-tags': json.dumps(authors)}


def get_default_author():
    authors = current_app.config.get('AUTHORS')
    return authors[0] if authors else getpass.getuser()

# classes


class BaseForm(Form):

    title = fields.StringField('Title', [validators.required()])
    summary = fields.TextAreaField('Summary')
    category = fields.Select2TagsField(
        'Category',
        [validators.CallableValidator(validate_category)],
        save_as_list=False,
        render_kw=get_category_kw,
        default=get_default_category
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
    content_type = fields.SelectField(
        'Type',
        [validators.required()],
        choices=[('article', 'Article'), ('page', 'Page')]
    )
    content_format = fields.SmartSelect2Field(
        'Format',
        [validators.required()],
        choices=get_content_format_choices
    )


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

    tags = fields.Select2TagsField('Tags', save_as_list=True)
    # todo: ^ provide settings.default_tags + db_query
    date = fields.DateTimeField(
        'Date',
        [validators.required()],
        default=dt.datetime.now
    )
    # todo: ^default should be now
    modified = fields.HiddenField('Modified')
    slug = fields.StringField('Slug')
    # TODO: validate slug collision
    language = fields.SmartSelect2Field(
        'Language',
        choices=lambda: [
            (lng, lng)
            for lng in current_app.config.get('BABEL_LANGUAGES', ['en'])
        ]
    )
    translations = fields.HiddenField('Translations')
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


class BaseFormat(object):
    identifier = None
    edit_form = BaseEditForm
    form_rules = None

    def get_edit_form(self, obj):
        return self.edit_form(get_form_data(), **obj)

    def get_identifier(self):
        return self.identifier or self.__class__.__name__

    def get_form_rules(self):
        if self.form_rules is not None:
            self.form_rules.append(
                rules.Field(
                    'csrf_token',
                    render_field='quokka_macros.render_hidden_field'
                )
            )
        return self.form_rules

    def before_save(self, form, model, is_created):
        """optional"""

    def after_save(self, form, model, is_created):
        """optional"""

    def extra_js(self):
        return []


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
    form_rules = [
        rules.FieldSet(('title', 'summary')),
        rules.Field('content'),
        rules.FieldSet(('category', 'authors', 'tags')),
        rules.FieldSet(('date',)),
        rules.FieldSet(('slug',)),
        rules.Field('published')
    ]

    def before_save(self, form, model, is_created):
        print('before save')

    def after_save(self, form, model, is_created):
        print('after save')

    def extra_js(self):
        return []
