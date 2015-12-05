#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from flask import url_for, redirect
from flask.ext.mistune import markdown

from quokka.core.db import db
from quokka.utils.shorturl import ShorterURL
from quokka.utils.settings import get_setting_value, get_site_url
from quokka.core.models.channel import Channeling
from quokka.core.models.custom_values import HasCustomValue
from quokka.core.models.subcontent import SubContent
from quokka.core.models.signature import (
    Tagged, Publishable, LongSlugged, ContentFormat, TemplateType
)

logger = logging.getLogger()


class ContentTemplateType(TemplateType, db.Document):
    """Define the content template type and its theme"""


class License(db.EmbeddedDocument):
    LICENSES = (('custom', 'custom'),
                ('creative_commons_by_nc_nd', 'creative_commons_by_nc_nd'))
    title = db.StringField(max_length=255)
    link = db.StringField(max_length=255)
    identifier = db.StringField(max_length=255, choices=LICENSES)


class ShortenedURL(db.EmbeddedDocument):
    original = db.StringField(max_length=255)
    short = db.StringField(max_length=255)

    def __str__(self):
        return self.short


###############################################################
# Base Content for every new content to extend. inheritance=True
###############################################################


class Content(HasCustomValue, Publishable, LongSlugged,
              Channeling, Tagged, ContentFormat, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    summary = db.StringField(required=False)
    template_type = db.ReferenceField(ContentTemplateType,
                                      required=False,
                                      reverse_delete_rule=db.NULLIFY)
    contents = db.ListField(db.EmbeddedDocumentField(SubContent))
    model = db.StringField()
    comments_enabled = db.BooleanField(default=True)
    license = db.EmbeddedDocumentField(License)
    shortened_url = db.EmbeddedDocumentField(ShortenedURL)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at'],
    }

    @classmethod
    def available_objects(cls, **filters):
        now = datetime.datetime.now()
        default_filters = {
            "published": True,
            'available_at__lte': now,
        }
        default_filters.update(filters)
        return cls.objects(**default_filters)

    def get_main_image_url(self, thumb=False,
                           default=None, identifier='mainimage'):
        """
        """
        if not isinstance(identifier, (list, tuple)):
            identifier = [identifier]

        for item in identifier:
            try:
                if not thumb:
                    path = self.contents.get(identifier=item).content.path
                else:
                    path = self.contents.get(identifier=item).content.thumb
                return url_for('quokka.core.media', filename=path)
            except Exception as e:
                logger.warning('get_main_image_url:' + str(e))

        return default

    def get_uid(self):
        return str(self.id)

    def get_themes(self):
        themes = self.channel.get_themes()
        theme = self.template_type and self.template_type.theme_name
        if theme:
            themes.insert(0, theme)
        return list(set(themes))

    def get_http_url(self):
        site_url = get_site_url()
        absolute_url = self.get_absolute_url()
        absolute_url = absolute_url[1:]
        return u"{}{}".format(site_url, absolute_url)

    def get_absolute_url(self, endpoint='quokka.core.detail'):
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

    def get_summary(self):
        if self.summary:
            return self.summary
        return self.get_text()

    def get_text(self):
        if hasattr(self, 'body'):
            text = self.body
        elif hasattr(self, 'description'):
            text = self.description
        else:
            text = self.summary or ""

        if self.content_format == "markdown":
            return markdown(text)
        else:
            return text

    def __unicode__(self):
        return self.title

    @property
    def short_url(self):
        return self.shortened_url.short if self.shortened_url else ''

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
        # all those functions should be in a dynamic pipeline
        self.validate_slug()
        self.validate_long_slug()
        self.heritage()
        self.populate_related_mpath()
        self.populate_channel_roles()
        self.populate_shorter_url()
        super(Content, self).save(*args, **kwargs)

    def pre_render(self, render_function, *args, **kwargs):
        return render_function(*args, **kwargs)

    def populate_shorter_url(self):
        if not self.published or not get_setting_value('SHORTENER_ENABLED'):
            return

        url = self.get_http_url()
        if not self.shortened_url or url != self.shortened_url.original:
            shortener = ShorterURL()
            self.shortened_url = ShortenedURL(original=url,
                                              short=shortener.short(url))


class Link(Content):
    link = db.StringField(required=True)
    force_redirect = db.BooleanField(default=True)
    increment_visits = db.BooleanField(default=True)
    visits = db.IntField(default=0)
    show_on_channel = db.BooleanField(default=False)

    def pre_render(self, render_function, *args, **kwargs):
        if self.increment_visits:
            self.visits = self.visits + 1
            self.save()
        if self.force_redirect:
            return redirect(self.link)
        return super(Link, self).pre_render(render_function, *args, **kwargs)
