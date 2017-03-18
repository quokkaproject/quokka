# coding: utf-8

from quokka.db import collection_index
from quokka.admin.views import ModelView
from quokka.admin.forms import fields, Form


class ContentForm(Form):
    """Base form for all contents"""

    title = fields.StringField('title')
    summary = fields.StringField('summary')
    category = fields.StringField('category')
    tags = fields.StringField('tags')
    slug = fields.StringField('slug')

    authors = fields.StringField('authors')
    date = fields.StringField('date')
    modified = fields.StringField('modified')

    lang = fields.StringField('lang')
    translations = fields.StringField('translations')
    status = fields.StringField('status')

    # metadata
    content_type = fields.StringField('type')


class ContentView(ModelView):
    """Base form for all contents"""
    form = ContentForm
    column_list = (
        'title',
        'category',
        'authors',
        'date',
        'modified',
        'lang',
        'status'
    )


def configure(app, db, admin):
    admin.register(
        collection_index,
        ContentView,
        name='Content'
    )
    return 'content'
