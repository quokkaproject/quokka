# coding: utf-8
from flask import current_app
from quokka.admin.forms import Form, fields, validators  # , rules
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

# classes


class BaseForm(Form):
    """Base form for all contents"""

    title = fields.StringField(_('Title'), [validators.required()])
    summary = fields.TextAreaField(_('Summary'))
    category = fields.Select2TagsField(_('Category'), save_as_list=False)
    authors = fields.Select2TagsField(_('Authors'), save_as_list=True)


class CreateForm(BaseForm):
    """Default create form where content type is chosen"""
    content_type = fields.SmartSelect2Field(
        _('Type'),
        choices=get_content_type_choices
    )


class BaseEditForm(BaseForm):
    """Edit form with all missing fields except `content`"""
    tags = fields.Select2TagsField(_('Tags'), save_as_list=True)
    date = fields.DateTimeField(_('Date'))
    modified = fields.HiddenField(_('Modified'))
    slug = fields.StringField(_('Slug'))
    lang = fields.SmartSelect2Field(
        _('Language'),
        choices=lambda: [
            (lng, lng)
            for lng in current_app.config.get('BABEL_LANGUAGES', ['en'])
        ]
    )
    translations = fields.HiddenField(_('Translations'))
    status = fields.HiddenField(_('Status'))


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
