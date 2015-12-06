#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
from flask import current_app
from quokka.core import TEXT_FORMATS
from quokka.core.db import db
from quokka.modules.accounts.models import User
from quokka.utils.text import slugify
from quokka.utils import get_current_user_for_models
from quokka.utils.settings import get_setting_value
from quokka.core.admin.utils import _l
from quokka.core.models.custom_values import HasCustomValue

###############################################################
# Commom extendable base classes
###############################################################


class ContentFormat(object):
    content_format = db.StringField(
        choices=TEXT_FORMATS,
        default=get_setting_value('DEFAULT_TEXT_FORMAT', 'html')
    )


class Dated(object):
    available_at = db.DateTimeField(default=datetime.datetime.now)
    available_until = db.DateTimeField(required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)


class Owned(object):
    created_by = db.ReferenceField(User)
    last_updated_by = db.ReferenceField(User)
    authors = db.ListField(db.ReferenceField(User))

    def get_authors(self):
        return set(self.authors + [self.created_by])

    @property
    def has_multiple_authors(self):
        return len(self.get_authors()) > 1


class Publishable(Dated, Owned):
    published = db.BooleanField(default=False)

    @property
    def is_available(self):
        now = datetime.datetime.now()
        return (
            self.published and
            self.available_at <= now and
            (self.available_until is None or
             self.available_until >= now)
        )

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()

        user = get_current_user_for_models()

        if not self.id and not self.created_by:
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
        if hasattr(self, 'is_homepage'):  # is channel
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
        else:  # is Content
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
                    _l("%(slug)s slug already exists",
                       slug=self.long_slug)
                )


class Tagged(object):
    tags = db.ListField(db.StringField(max_length=50))


class Ordered(object):
    order = db.IntField(required=True, default=1)


class TemplateType(HasCustomValue):
    title = db.StringField(max_length=255, required=True)
    identifier = db.StringField(max_length=255, required=True, unique=True)
    template_suffix = db.StringField(max_length=255, required=True)
    theme_name = db.StringField(max_length=255, required=False)

    def __unicode__(self):
        return self.title
