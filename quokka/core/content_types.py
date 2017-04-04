# coding: utf-8
import datetime as dt
from flask import current_app
from quokka.admin.forms import (
    Form, fields, validators
)
from werkzeug.utils import import_string
from quokka.admin.utils import _
from flask_admin.helpers import get_form_data


# Utils

def get_content_types(instances=False):
    content_types = current_app.config.get(
        'CONTENT_TYPES',
        {
          'markdown': {
              'choice_text': 'Markdown',
              'help_text': 'Markdown text editor',
              'content_type_class': 'quokka.core.content_types.MarkdownContentType'  # noqa
          }
        }
    )
    if instances:
        for identifier, data in content_types:
            data['content_type_instance'] = import_string(
                data['content_type_class']
            )()
    return content_types


def get_content_type_choices():
    content_types = get_content_types()
    return [
        # ('value', 'TEXT')
        (identifier, data['choice_text'])
        for identifier, data
        in content_types.items()
    ]


def get_edit_form(obj):
    content_types = get_content_types()
    try:
        obj_content_type = content_types[obj['content_type']]
        content_type = import_string(obj_content_type['content_type_class'])()
        return content_type.get_edit_form(obj)
    except (KeyError):
        return PlainContentType().get_edit_form(obj)


def validate_category(form, field):
    if field.data is not None:
        items = field.data.split(',')
        if len(items) > 1:
            return _(u'You can select only one category')

# classes


class BaseForm(Form):
    """Base form for all contents"""

    title = fields.StringField(_('Title'), [validators.required()])
    # todo: validade existing category/title
    summary = fields.TextAreaField(_('Summary'))
    category = fields.Select2TagsField(
        _('Category'),
        [
            validators.required(),
            validators.CallableValidator(validate_category)
        ],
        save_as_list=False,
        render_kw={'data-tags': '["hello", "world"]'},
        # todo: ^ settings.default_categories + db_query
        default='general'
        # todo: default should come from settings
    )
    authors = fields.Select2TagsField(
        _('Authors'),
        [validators.required()],
        save_as_list=True,
        render_kw={'data-tags': '["Bruno Rocha", "Karla Magueta"]'},
        # todo: settings.default_authors + current + db_query
        default=['Bruno Rocha']
        # todo: default should be current user if auth else O.S user else ?
    )


class CreateForm(BaseForm):
    """Default create form where content type is chosen"""
    content_type = fields.SmartSelect2Field(
        _('Type'),
        [validators.required()],
        choices=get_content_type_choices
    )


class BaseEditForm(BaseForm):
    """Edit form with all missing fields except `content`"""
    tags = fields.Select2TagsField(_('Tags'), save_as_list=True)
    # todo: ^ provide settings.default_tags + db_query
    date = fields.DateTimeField(
        _('Date'),
        [validators.required()],
        default=dt.datetime.now
    )
    # todo: ^default should be now
    modified = fields.HiddenField(_('Modified'))
    # todo: ^populate on save
    slug = fields.StringField(_('Slug'))
    # todo: create based on category / title
    lang = fields.SmartSelect2Field(
        _('Language'),
        choices=lambda: [
            (lng, lng)
            for lng in current_app.config.get('BABEL_LANGUAGES', ['en'])
        ]
    )
    translations = fields.HiddenField(_('Translations'))
    # todo: ^ create action 'add translation'
    status = fields.HiddenField(_('Status'))
    # todo: ^ published | draft


class BaseContentType(object):
    identifier = None
    help_text = ''
    edit_form = BaseEditForm

    def get_edit_form(self, obj):
        return self.edit_form(get_form_data(), **obj)

    def get_identifier(self):
        return self.identifier or self.__class__.__name__

# Customs


class PlainEditForm(BaseEditForm):
    content = fields.TextAreaField(_('Content'))


class PlainContentType(BaseContentType):
    edit_form = PlainEditForm


class HTMLEditForm(BaseEditForm):
    content = fields.TextAreaField(_('Content'))


class HTMLContentType(BaseContentType):
    edit_form = HTMLEditForm


class MarkdownEditForm(BaseEditForm):
    content = fields.TextAreaField(_('Content'))


class MarkdownContentType(BaseContentType):
    edit_form = MarkdownEditForm
