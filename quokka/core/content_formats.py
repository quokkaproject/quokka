# coding: utf-8
import datetime as dt
from flask import current_app
from quokka.admin.forms import (
    Form, fields, validators, rules, READ_ONLY
)
from werkzeug.utils import import_string
from quokka.admin.utils import _
from flask_admin.helpers import get_form_data


# Utils

def get_content_formats(instances=False):
    content_formats = current_app.config.get(
        'CONTENT_FORMATS',
        {
          'markdown': {
              'choice_text': 'Markdown',
              'help_text': 'Markdown text editor',
              'content_format_class': 'quokka.core.content_formats.MarkdownFormat'  # noqa
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
            return _(u'You can select only one category')

# classes


class BaseForm(Form):

    title = fields.StringField(_('Title'), [validators.required()])
    # todo: validade existing category/title
    summary = fields.TextAreaField(_('Summary'))
    category = fields.Select2TagsField(
        _('Category'),
        [validators.CallableValidator(validate_category)],
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
    """Default create form where content format is chosen"""
    content_type = fields.SelectField(
        _('Type'),
        [validators.required()],
        choices=[('article', _('Article')), ('page', _('Page'))]
    )
    content_format = fields.SmartSelect2Field(
        _('Format'),
        [validators.required()],
        choices=get_content_format_choices
    )


class BaseEditForm(BaseForm):
    """Edit form with all missing fields except `content`"""

    content_type = fields.PassiveStringField(
        _('Type'),
        render_kw=READ_ONLY
    )
    content_format = fields.PassiveStringField(_('Format'), render_kw=READ_ONLY)

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
    language = fields.SmartSelect2Field(
        _('Language'),
        choices=lambda: [
            (lng, lng)
            for lng in current_app.config.get('BABEL_LANGUAGES', ['en'])
        ]
    )
    translations = fields.HiddenField(_('Translations'))
    # todo: ^ create action 'add translation'
    published = fields.BooleanField(
        _('Status'),
        render_kw={
            'data-toggle': "toggle",
            'data-on': _("Published"),
            'data-off': _("Draft"),
            "data-onstyle": 'success'
        }
    )
    # todo: ^ published | draft


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

    def before_save(self, form, model):
        """optional"""

    def after_save(self, form, model):
        """optional"""

    def extra_js(self):
        return []


# Customs


class PlainEditForm(BaseEditForm):
    content = fields.TextAreaField(_('Plain Content'))


class PlainFormat(BaseFormat):
    edit_form = PlainEditForm


class HTMLEditForm(BaseEditForm):
    content = fields.TextAreaField(_('HTML Content'))


class HTMLFormat(BaseFormat):
    edit_form = HTMLEditForm


class MarkdownEditForm(BaseEditForm):
    content = fields.TextAreaField(_('Markdown Content'))


class MarkdownFormat(BaseFormat):
    edit_form = MarkdownEditForm
    form_rules = [
        rules.FieldSet(('title', 'summary')),
        rules.Field('content'),
        rules.FieldSet(('category', 'authors', 'tags')),
        rules.FieldSet(('date', 'language')),
        rules.FieldSet(('slug', 'content_type', 'content_format')),
        rules.Field('published')
    ]

    def before_save(self, form, model):
        print('before save')

    def after_save(self, form, model):
        print('after save')

    def extra_js(self):
        return []
