#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask_mistune import markdown

from quokka.core.db import db
from quokka.core.models.custom_values import HasCustomValue
from quokka.core.models.signature import (
    Tagged, Publishable, LongSlugged, ContentFormat, TemplateType
)
from quokka.core.admin.utils import _l
from quokka.utils.settings import get_site_url
logger = logging.getLogger()


class ChannelConfigs(object):
    content_filters = db.DictField(required=False, default=lambda: {})
    inherit_parent = db.BooleanField(default=True)


class ChannelType(TemplateType, ChannelConfigs, db.DynamicDocument):
    """Define the channel template type and its filters"""


class ContentProxy(db.DynamicDocument):
    content = db.GenericReferenceField(required=True, unique=True)

    def __unicode__(self):
        return self.content.title


class Channel(Tagged, HasCustomValue, Publishable, LongSlugged,
              ChannelConfigs, ContentFormat, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    description = db.StringField()
    show_in_menu = db.BooleanField(default=False)
    is_homepage = db.BooleanField(default=False)
    roles = db.ListField(
        db.ReferenceField('Role', reverse_delete_rule=db.PULL))
    include_in_rss = db.BooleanField(default=True)
    indexable = db.BooleanField(default=True)
    canonical_url = db.StringField()
    order = db.IntField(default=0)

    parent = db.ReferenceField('self', required=False, default=None,
                               reverse_delete_rule=db.DENY)

    per_page = db.IntField(default=0)
    aliases = db.ListField(db.StringField(), default=[])
    channel_type = db.ReferenceField(ChannelType, required=False,
                                     reverse_delete_rule=db.NULLIFY)

    redirect_url = db.StringField(max_length=255)
    render_content = db.ReferenceField(ContentProxy,
                                       required=False,
                                       reverse_delete_rule=db.NULLIFY)
    sort_by = db.ListField(db.StringField(), default=[])
    link_in_menu = db.BooleanField(default=True)

    meta = {
        'ordering': ['order', 'title'],
    }

    def get_text(self):
        if self.content_format == "markdown":
            return markdown(self.description)
        else:
            return self.description

    def get_content_filters(self):
        filters = {}
        if self.channel_type and self.channel_type.content_filters:
            filters.update(self.channel_type.content_filters)
        if self.content_filters:
            filters.update(self.content_filters)
        return filters

    def get_ancestors_count(self):
        """
        return how many ancestors this node has based on slugs
        """
        return len(self.get_ancestors_slugs())

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
            logger.info("There is no homepage: %s", e.message)
            return None
        else:
            if not attr:
                return homepage
            else:
                return getattr(homepage, attr, homepage)

    def __unicode__(self):
        return self.long_slug

    def get_absolute_url(self, *args, **kwargs):
        if self.is_homepage:
            return "/"
        return "/{0}/".format(self.long_slug)

    def get_canonical_url(self, *args, **kwargs):
        """
        This method should be reviewed
        Canonical URL is the preferred URL for a content
        when the content can be served by multiple URLS
        In the case of channels it will never happen
        until we implement the channel alias feature
        """
        if self.is_homepage:
            return "/"
        return self.get_absolute_url()

    def get_http_url(self):
        site_url = get_site_url()
        absolute_url = self.get_absolute_url()
        absolute_url = absolute_url[1:]
        return u"{0}{1}".format(site_url, absolute_url)

    def clean(self):
        homepage = Channel.objects(is_homepage=True)
        if self.is_homepage and homepage and self not in homepage:
            raise db.ValidationError(_l("Home page already exists"))
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
        """
        Need to Detect if self.long_slug and self.mpath has changed.
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
        if not self.channel_type:
            self.channel_type = ChannelType.objects.first()
        super(Channel, self).save(*args, **kwargs)


class Channeling(object):
    channel = db.ReferenceField(Channel, required=True,
                                reverse_delete_rule=db.DENY)
    related_channels = db.ListField(
        db.ReferenceField('Channel', reverse_delete_rule=db.PULL)
    )
    related_mpath = db.ListField(db.StringField())
    show_on_channel = db.BooleanField(default=True)
    channel_roles = db.ListField(db.StringField())

    def populate_related_mpath(self):
        self.related_mpath = [rel.mpath for rel in self.related_channels]

    def populate_channel_roles(self):
        self.channel_roles = [role.name for role in self.channel.roles]


class ChannelingNotRequired(Channeling):
    channel = db.ReferenceField(Channel, required=False,
                                reverse_delete_rule=db.NULLIFY)
