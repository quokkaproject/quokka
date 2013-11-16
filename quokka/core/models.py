#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import datetime
import random
from flask import url_for, current_app
from flask.ext.admin.babel import lazy_gettext
from quokka.core.db import db
from quokka.core.fields import MultipleObjectsReturned
from quokka.modules.accounts.models import User
from quokka.utils.text import slugify
from quokka.utils import get_current_user

logger = logging.getLogger()


###############################################################
# Commom extendable base classes
###############################################################

class Dated(object):
    available_at = db.DateTimeField(default=datetime.datetime.now)
    available_until = db.DateTimeField(required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)


class Owned(object):
    created_by = db.ReferenceField(User)
    last_updated_by = db.ReferenceField(User)


class Publishable(Dated, Owned):
    published = db.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()

        user = get_current_user()
        if not self.id:
            self.created_by = user
        self.last_updated_by = user

        super(Publishable, self).save(*args, **kwargs)


class Slugged(object):
    slug = db.StringField(max_length=255, required=True)

    def validate_slug(self, title=None):
        if self.slug:
            self.slug = slugify(self.slug)
        else:
            self.slug = slugify(title or self.title)


class LongSlugged(Slugged):
    long_slug = db.StringField(unique=True, required=True)
    mpath = db.StringField()

    def _create_mpath_long_slug(self):
        if isinstance(self, Channel):
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
        elif isinstance(self, Content):
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
    def value(self, value):
        self.rawvalue = self.REVERSE_FORMATTERS.get(self.formatter,
                                                    self.STR_FORMATTER)(value)

    def clean(self):
        try:
            self.value
        except Exception as e:
            # raise base exception because Flask-Admin can't handle the output
            # for some specific Exceptions of Mongoengine
            raise Exception(e.message)
        super(CustomValue, self).clean()

    def __unicode__(self):
        return u"{s.name} -> {s.value}".format(s=self)


class HasCustomValue(object):
    values = db.ListField(db.EmbeddedDocumentField(CustomValue))

    def get_values_tuple(self):
        return [(value.name, value.value, value.formatter)
                for value in self.values]

    def clean(self):
        current_names = [value.name for value in self.values]
        for name in current_names:
            if current_names.count(name) > 1:
                raise Exception(lazy_gettext("%(name)s already exists",
                                             name=name))
        super(HasCustomValue, self).clean()


class Ordered(object):
    order = db.IntField(required=True, default=1)


class ChannelConfigs(object):
    content_filters = db.DictField(required=False, default=lambda: {})
    inherit_parent = db.BooleanField(default=True)


class TemplateType(HasCustomValue):
    title = db.StringField(max_length=255, required=True)
    identifier = db.StringField(max_length=255, required=True, unique=True)
    template_suffix = db.StringField(max_length=255, required=True)
    theme_name = db.StringField(max_length=255, required=False)

    def __unicode__(self):
        return self.title


class ChannelType(TemplateType, ChannelConfigs, db.DynamicDocument):
    """Define the channel template type and its filters"""


class ContentProxy(db.DynamicDocument):
    content = db.GenericReferenceField(required=True, unique=True)

    def __unicode__(self):
        return self.content.title


class Channel(Tagged, HasCustomValue, Publishable, LongSlugged,
              ChannelConfigs, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    description = db.StringField()
    show_in_menu = db.BooleanField(default=False)
    is_homepage = db.BooleanField(default=False)
    include_in_rss = db.BooleanField(default=True)
    indexable = db.BooleanField(default=True)
    canonical_url = db.StringField()
    order = db.IntField(default=0)

    parent = db.ReferenceField('self', required=False, default=None,
                               reverse_delete_rule=db.DENY)

    per_page = db.IntField(default=0)
    aliases = db.ListField(db.StringField())
    channel_type = db.ReferenceField(ChannelType, required=False,
                                     reverse_delete_rule=db.NULLIFY)

    redirect_url = db.StringField(max_length=255)
    render_content = db.ReferenceField(ContentProxy,
                                       required=False,
                                       reverse_delete_rule=db.NULLIFY)

    meta = {
        'ordering': ['order', 'title']
    }

    def get_content_filters(self):
        filters = {}
        if self.channel_type and self.channel_type.content_filters:
            filters.update(self.channel_type.content_filters)
        if self.content_filters:
            filters.update(self.content_filters)
        return filters

    def get_ancestors_slugs(self):
        """return ancestors slugs including self as 1st item
        >>> channel = Channel(long_slug='articles/technology/programming')
        >>> channel.get_ancestors_slugs()
        ['articles/technology/programming',
         'articles/technology',
         'articles']
        """

        channel_list = []
        channel_slugs = self.long_slug.split('/')
        while channel_slugs:
            channel_list.append("/".join(channel_slugs))
            channel_slugs.pop()
        return channel_list

    def get_ancestors(self, **kwargs):
        """return all ancestors includind self as 1st item"""
        channel_list = self.get_ancestors_slugs()
        ancestors = self.__class__.objects(
            long_slug__in=channel_list,
            **kwargs
        ).order_by('-long_slug')
        return ancestors

    def get_children(self, **kwargs):
        """return direct children 1 level depth"""
        return self.__class__.objects(
            parent=self, **kwargs
        ).order_by('long_slug')

    def get_descendants(self, **kwargs):
        """return all descendants including self as 1st item"""
        return self.__class__.objects(
            __raw__={'mpath': {'$regex': '^{0}'.format(self.mpath)}}
        ).order_by('long_slug')

    def get_themes(self):
        return list({
            c.channel_type.theme_name
            for c in self.get_ancestors(channel_type__ne=None)
            if c.channel_type and c.channel_type.theme_name
        })

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

    def get_absolute_url(self, *args, **kwargs):
        return "/{0}/".format(self.long_slug)

    def get_canonical_url(self, *args, **kwargs):
        if self.is_homepage:
            return "/"
        return self.get_absolute_url()

    def clean(self):
        homepage = Channel.objects(is_homepage=True)
        if self.is_homepage and homepage and not self in homepage:
            raise db.ValidationError(lazy_gettext("Home page already exists"))
        super(Channel, self).clean()

    def validate_render_content(self):
        if self.render_content and \
                not isinstance(self.render_content, ContentProxy):
            self.render_content, created = ContentProxy.objects.get_or_create(
                content=self.render_content)
        else:
            self.render_content = None

    def heritage(self):
        """populate inheritance from parent channels"""
        parent = self.parent
        if not parent or not self.inherit_parent:
            return

        self.content_filters = self.content_filters or parent.content_filters
        self.include_in_rss = self.include_in_rss or parent.include_in_rss
        self.show_in_menu = self.show_in_menu or parent.show_in_menu
        self.indexable = self.indexable or parent.indexable
        self.channel_type = self.channel_type or parent.channel_type

    def update_descendants_and_contents(self):
        """TODO:
        Detect if self.long_slug and self.mpath has changed.
        if so, update every descendant using get_descendatns method
        to query.
        Also update long_slug and mpath for every Content in this channel
        This needs to be done by default in araw immediate way, but if
        current_app.config.get('ASYNC_SAVE_MODE') is True it will delegate
        all those tasks to celery."""

    def save(self, *args, **kwargs):
        self.validate_render_content()
        self.validate_slug()
        self.validate_long_slug()
        self.heritage()
        self.update_descendants_and_contents()
        super(Channel, self).save(*args, **kwargs)


class Channeling(object):
    channel = db.ReferenceField(Channel, required=True,
                                reverse_delete_rule=db.DENY)
    related_channels = db.ListField(
        db.ReferenceField('Channel', reverse_delete_rule=db.PULL)
    )
    show_on_channel = db.BooleanField(default=True)


class ChannelingNotRequired(Channeling):
    channel = db.ReferenceField(Channel, required=False,
                                reverse_delete_rule=db.NULLIFY)


class Config(HasCustomValue, Publishable, db.DynamicDocument):
    group = db.StringField(max_length=255)
    description = db.StringField()

    @classmethod
    def get(cls, group, name=None, default=None):

        try:
            instance = cls.objects.get(group=group)
        except:
            return None

        if not name:
            ret = instance.values
            if group == 'settings':
                ret = {}
                ret.update(current_app.config)
                ret.update({item.name: item.value for item in instance.values})
        else:
            try:
                ret = instance.values.get(name=name).value
            except (MultipleObjectsReturned, AttributeError):
                ret = None

        if not ret and group == 'settings' and name is not None:
            ret = current_app.config.get(name)

        return ret or default

    def save(self, *args, **kwargs):
        super(Config, self).save(*args, **kwargs)

        # Try to update the config for the running app
        # AFAIK Flask apps are not thread safe
        # TODO: do it in a signal
        try:
            if self.group == 'settings':
                _settings = {i.name: i.value for i in self.values}
                current_app.config.update(_settings)
        except:
            logger.warning("Cant update app settings")

    def __unicode__(self):
        return self.group


class Quokka(Dated, Slugged, db.DynamicDocument):
    """ Hidden collection """


class ContentTemplateType(TemplateType, db.Document):
    """Define the content template type and its theme"""


class SubContentPurpose(db.Document):
    title = db.StringField(max_length=255, required=True)
    identifier = db.StringField(max_length=255, required=True, unique=True)
    module = db.StringField()

    def save(self, *args, **kwargs):
        self.identifier = slugify(self.identifier or self.title)
        super(SubContentPurpose, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class SubContent(Publishable, Ordered, db.EmbeddedDocument):
    """Content can have inner contents
    Its useful for any kind of relation with Content childs
    Images, ImageGalleries, RelatedContent, Attachments, Media
    """

    content = db.ReferenceField('Content', required=True)
    caption = db.StringField()
    purpose = db.ReferenceField(SubContentPurpose, required=True)
    identifier = db.StringField()

    meta = {
        'ordering': ['order'],
        'indexes': ['order']
    }

    def clean(self):
        self.identifier = self.purpose.identifier

    def __unicode__(self):
        return self.content and self.content.title or self.caption


###############################################################
# Base Content for every new content to extend. inheritance=True
###############################################################


class Content(HasCustomValue, Publishable, LongSlugged,
              Channeling, Tagged, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    summary = db.StringField(required=False)
    template_type = db.ReferenceField(ContentTemplateType,
                                      required=False,
                                      reverse_delete_rule=db.NULLIFY)
    contents = db.ListField(db.EmbeddedDocumentField(SubContent))
    model = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

    def get_main_image_url(self, thumb=False, default=None):
        try:
            #main_image = SubContentPurpose.objects.get(identifier='mainimage')
            if not thumb:
                path = self.contents.get(identifier='mainimage').content.path
            else:
                path = self.contents.get(identifier='mainimage').content.thumb
            return url_for('media', filename=path)
        except Exception as e:
            logger.warning(str(e))
            return default

    def get_uid(self):
        return str(self.id)

    def get_themes(self):
        themes = self.channel.get_themes()
        theme = self.template_type and self.template_type.theme_name
        if theme:
            themes.insert(0, theme)
        return list(set(themes))

    def get_absolute_url(self, endpoint='detail'):
        if self.channel.is_homepage:
            long_slug = self.slug
        else:
            long_slug = self.long_slug

        try:
            return url_for(self.URL_NAMESPACE, long_slug=long_slug)
        except:
            return url_for(endpoint, long_slug=long_slug)

    def get_canonical_url(self, *args, **kwargs):
        return self.get_absolute_url()

    def get_recommendations(self, limit=3, ordering='-created_at', *a, **k):
        now = datetime.datetime.now()
        filters = {
            'published': True,
            'available_at__lte': now,
            "id__ne": self.id
        }
        contents = Content.objects(**filters).filter(tags__in=self.tags or [])

        return contents.order_by(ordering)[:limit]

    def get_text(self):
        if hasattr(self, 'body'):
            return self.body
        elif hasattr(self, 'description'):
            return self.description
        else:
            return self.summary

    def __unicode__(self):
        return self.title

    @property
    def model_name(self):
        return self.__class__.__name__.lower()

    @property
    def module_name(self):
        module = self.__module__
        module_name = module.replace('quokka.modules.', '').split('.')[0]
        return module_name

    def heritage(self):
        self.model = "{0}.{1}".format(self.module_name, self.model_name)

    def save(self, *args, **kwargs):
        self.validate_slug()
        self.validate_long_slug()
        self.heritage()
        super(Content, self).save(*args, **kwargs)


class Link(Content):
    link = db.StringField(required=True)
