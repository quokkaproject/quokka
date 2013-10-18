#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import datetime
import random
from flask import url_for, current_app
from flask.ext.security import current_user
from flask.ext.admin.babel import lazy_gettext
from flask.ext.admin import form
from jinja2 import Markup
from quokka.core.db import db
from quokka import admin
from quokka.core.admin.models import ModelAdmin
from quokka.modules.accounts.models import User
from quokka.utils.text import slugify
from quokka import settings

logger = logging.getLogger()


###############################################################
# Commom extendable base classes
###############################################################


class Publishable(object):
    published = db.BooleanField(default=False)
    available_at = db.DateTimeField(default=datetime.datetime.now)
    available_until = db.DateTimeField(required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    created_by = db.ReferenceField(User, reverse_delete_rule=db.DENY)
    last_updated_by = db.ReferenceField(User, reverse_delete_rule=db.DENY)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()

        try:
            user = User.objects.get(id=current_user.id)
            if not self.id:
                self.created_by = user
            self.last_updated_by = user
        except Exception as e:
            logger.warning("No user to save the model: %s" % e.message)

        super(Publishable, self).save(*args, **kwargs)


class Slugged(object):
    slug = db.StringField(max_length=255, required=True)
    long_slug = db.StringField(unique=True, required=True)
    mpath = db.StringField()

    def _create_mpath_long_slug(self):
        try:
            if self.parent and self.parent != self:
                self.long_slug = "/".join(
                    [self.parent.long_slug, self.slug]
                )

                self.mpath = "".join(
                    [self.parent.mpath, self.slug, ',']
                )
            else:
                self.long_slug = self.slug
                self.mpath = ",%s," % self.slug
        except:
            logger.info("excepting to content validate_long_slug")
            self.long_slug = "/".join(
                [self.channel.long_slug, self.slug]
            )

            self.mpath = "".join([self.channel.mpath, self.slug, ','])

    def validate_long_slug(self):

        self._create_mpath_long_slug()

        filters = dict(long_slug=self.long_slug)
        if self.id:
            filters['id__ne'] = self.id

        exist = self.__class__.objects(**filters)
        if exist.count():
            if current_app.config.get('SMART_SLUG_ENABLED', False):
                self.slug = "{0}-{1}".format(self.slug, random.getrandbits(32))
                self._create_mpath_long_slug()
            else:
                raise db.ValidationError(
                    lazy_gettext("%(slug)s slug already exists",
                                 slug=self.long_slug)
                )

    def validate_slug(self, title=None):
        if self.slug:
            self.slug = slugify(self.slug)
        else:
            self.slug = slugify(title or self.title)


class Comment(db.EmbeddedDocument):
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
    published = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    created_by = db.ReferenceField(User)  # reverse_delete_rule not supported

    def __unicode__(self):
        return "{0}-{1}...".format(self.author, self.body[:10])

    meta = {
        'indexes': ['-created_at', '-available_at'],
        'ordering': ['-created_at']
    }


class Commentable(object):
    comments = db.ListField(db.EmbeddedDocumentField(Comment))


class Tagged(object):
    tags = db.ListField(db.StringField(max_length=50))


class CustomValue(db.EmbeddedDocument):

    FORMATS = (
        ('json', "json"),
        ('text', "text"),
        ('int', "int"),
        ('float', "float"),
    )

    DEFAULT_FORMATTER = lambda value: value

    FORMATTERS = {
        'json': lambda value: json.loads(value),
        'text': DEFAULT_FORMATTER,
        'int': lambda value: int(value),
        'float': lambda value: float(value)
    }

    REVERSE_FORMATTERS = {
        'json': lambda value:
        value if isinstance(value, str) else json.dumps(value),
        'text': DEFAULT_FORMATTER,
        'int': DEFAULT_FORMATTER,
        'float': DEFAULT_FORMATTER
    }

    name = db.StringField(max_length=50, required=True)
    rawvalue = db.StringField(verbose_name=lazy_gettext("Value"),
                              required=True)
    formatter = db.StringField(choices=FORMATS, default="text", required=True)

    @property
    def value(self):
        return self.FORMATTERS.get(self.formatter,
                                   self.DEFAULT_FORMATTER)(self.rawvalue)

    @value.setter
    def value(self, value):  # lint:ok
        self.rawvalue = self.REVERSE_FORMATTERS.get(self.formatter,
                                                    self.STR_FORMATTER)(value)

    def clean(self):
        try:
            self.value
        except Exception as e:
            raise Exception(e.message)
        super(CustomValue, self).clean()

    def __unicode__(self):
        return self.name


class HasCustomValue(object):
    values = db.ListField(db.EmbeddedDocumentField(CustomValue))

    def clean(self):
        current_names = [value.name for value in self.values]
        for name in current_names:
            if current_names.count(name) > 1:
                raise Exception(lazy_gettext("%(name)s already exists",
                                             name=name))
        super(HasCustomValue, self).clean()


class Imaged(object):
    main_image = db.ReferenceField("Image", required=False,
                                   reverse_delete_rule=db.NULLIFY)
    main_image_caption = db.StringField(max_length=255)


class ChannelConfigs(object):
    content_filters = db.DictField(required=False)
    inherit_parent = db.BooleanField(default=False)


class TemplateType(HasCustomValue):
    title = db.StringField(max_length=255, required=True)
    identifier = db.StringField(max_length=255, required=True, unique=True)
    template_suffix = db.StringField(max_length=255, required=True)
    theme_name = db.StringField(max_length=255, required=False)

    def __unicode__(self):
        return self.title


class ChannelType(TemplateType, ChannelConfigs, db.DynamicDocument):
    """Define the channel template type and its filters"""


class Channel(HasCustomValue, Publishable, Slugged,
              ChannelConfigs, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    description = db.StringField()
    show_in_menu = db.BooleanField(default=False)
    is_homepage = db.BooleanField(default=False)
    include_in_rss = db.BooleanField(default=False)
    indexable = db.BooleanField(default=True)
    canonical_url = db.StringField()
    order = db.IntField(default=0)

    # MPTT
    parent = db.ReferenceField('self', required=False, default=None,
                               reverse_delete_rule=db.DENY)

    aliases = db.ListField(db.StringField())
    channel_type = db.ReferenceField(ChannelType, required=False,
                                     reverse_delete_rule=db.NULLIFY)

    render_content = db.StringField(max_length=255, required=False)

    def get_ancestors(self, menu=True):
        return self.__class__.objects(parent=self, show_in_menu=menu)

    @classmethod
    def get_homepage(cls, attr=None):
        try:
            homepage = cls.objects.get(is_homepage=True)
        except Exception as e:
            logger.info("There is no homepage: %s" % e.message)
            return None
        else:
            if not attr:
                return homepage
            else:
                return getattr(homepage, attr, homepage)

    def __unicode__(self):
        return self.long_slug

    def get_absolute_url(self):
        return "/{0}/".format(self.long_slug)

    def clean(self):
        homepage = Channel.objects(is_homepage=True)
        if self.is_homepage and homepage and not self in homepage:
            raise db.ValidationError(lazy_gettext("Home page already exists"))
        super(Channel, self).clean()

    def save(self, *args, **kwargs):

        self.validate_slug()
        self.validate_long_slug()

        super(Channel, self).save(*args, **kwargs)


class Channeling(object):
    channel = db.ReferenceField(Channel, required=True,
                                reverse_delete_rule=db.DENY)
    # Objects can be in only one main channel it gives an url
    # but the objects can also be relates to other channels
    related_channels = db.ListField(
        db.ReferenceField('Channel', reverse_delete_rule=db.PULL)
    )
    show_on_channel = db.BooleanField(default=True)


class ChannelingNotRequired(Channeling):
    channel = db.ReferenceField(Channel, required=False,
                                reverse_delete_rule=db.NULLIFY)


class Archive(HasCustomValue, Publishable, ChannelingNotRequired,
              Tagged, Slugged, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    summary = db.StringField(required=False)
    path = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

    def __unicode__(self):
        return self.title


class File(Archive):
    pass


class Image(Archive):
    pass


class Config(HasCustomValue, Publishable, db.DynamicDocument):
    group = db.StringField(max_length=255)
    description = db.StringField()

    def save(self, *args, **kwargs):
        super(Config, self).save(*args, **kwargs)

        # Try to update the config for the running app
        # AFAIK Flask apps are not thread safe
        # TODO: do it in a signal
        try:
            if self.group == 'settings':
                settings = {i.name: i.value for i in self.values}
                current_app.config.update(settings)
        except:
            logger.warning("Cant update app settings")

    def __unicode__(self):
        return self.group


class ContentTemplateType(TemplateType, db.DynamicDocument):
    """Define the channel template type and its filters"""


###############################################################
# Base Content for every new content to extend. inheritance=True
###############################################################


class Content(HasCustomValue, Imaged, Publishable, Slugged, Commentable,
              Channeling, Tagged, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    summary = db.StringField(required=False)
    template_type = db.ReferenceField(ContentTemplateType,
                                      required=False,
                                      reverse_delete_rule=db.NULLIFY)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

    def get_absolute_url(self, endpoint='detail'):
        if self.channel.is_homepage:
            long_slug = self.slug
        else:
            long_slug = self.long_slug

        try:
            return url_for(self.URL_NAMESPACE, long_slug=long_slug)
        except:
            return url_for(endpoint, long_slug=long_slug)

    def __unicode__(self):
        return self.title

    @property
    def content_type(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):

        self.validate_slug()
        self.validate_long_slug()

        super(Content, self).save(*args, **kwargs)


###############################################################
# Admin views
###############################################################

class ConfigAdmin(ModelAdmin):
    roles_accepted = ('admin', 'developer')
    column_list = ("group", "description", "published",
                   "created_at", "updated_at")
    column_filters = ("group", "description")
    form_columns = ("group", "description", "published", "values")

admin.register(Config, ConfigAdmin, category="Settings")


class ChannelTypeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')

admin.register(ChannelType, ChannelTypeAdmin, category="Settings")


class ContentTemplateTypeAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')

admin.register(ContentTemplateType,
               ContentTemplateTypeAdmin,
               category="Settings")


class ChannelAdmin(ModelAdmin):
    edit_template = 'admin/custom/edit.html'
    create_template = 'admin/custom/create.html'
    roles_accepted = ('admin', 'editor')
    column_list = ('title', 'long_slug', 'is_homepage',
                   'channel_type', 'created_at', 'available_at', 'published')
    column_filters = ['published', 'is_homepage', 'include_in_rss',
                      'show_in_menu', 'indexable']
    column_searchable_list = ('title', 'description')
    form_columns = ['title', 'slug', 'description', 'parent', 'is_homepage',
                    'include_in_rss', 'indexable', 'show_in_menu', 'order',
                    'published', 'canonical_url', 'values', 'channel_type',
                    'inherit_parent', 'content_filters', 'available_at',
                    'available_until', 'render_content']
    column_formatters = {'created_at': ModelAdmin.formatters.get('datetime'),
                         'available_at': ModelAdmin.formatters.get('datetime')}
    form_subdocuments = {}

    form_widget_args = {
        'description': {
            'rows': 20,
            'cols': 20,
            'class': 'text_editor',
            'style': "margin: 0px; width: 400px; height: 250px;"
        },
        'title': {'style': 'width: 400px'},
        'slug': {'style': 'width: 400px'},
    }


admin.register(Channel, ChannelAdmin, category="Content")


class FileAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')
    column_list = ('title', 'path', 'published')
    form_columns = ['title', 'path', 'published']

    form_overrides = {
        'path': form.FileUploadField
    }

    form_args = {
        'path': {
            'label': 'File',
            'base_path': os.path.join(settings.MEDIA_ROOT, 'files')
        }
    }


admin.register(File, FileAdmin, category='Content')


class ImageAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')
    column_list = ('title', 'path', 'thumb', 'published')
    form_columns = ['title', 'path', 'published']

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup(
            '<img src="%s">' % url_for(
                'media',
                filename="images/{0}".format(form.thumbgen_filename(
                    model.path))
            )
        )

    column_formatters = {
        'thumb': _list_thumbnail
    }

    form_extra_fields = {
        'path': form.ImageUploadField(
            'Image',
            base_path=os.path.join(settings.MEDIA_ROOT, 'images'),
            thumbnail_size=(100, 100, True),
            endpoint="media"
        )
    }


admin.register(Image, ImageAdmin, category='Content')
