#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import url_for
from quokka.core.db import db
from quokka import admin
from quokka.modules.accounts.models import User

###############################################################
# Commom extendable base classes
###############################################################


class Publishable(object):
    published = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    created_by = db.ReferenceField(User)
    last_updated_by = db.ReferenceField(User)


class Slugged(object):
    slug = db.StringField(max_length=255, required=True)


class Comment(db.EmbeddedDocument, Publishable):
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
    published = db.BooleanField(default=True)

    def __unicode__(self):
        return "{}-{}...".format(self.author, self.body[:10])

    meta = {
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }


class Commentable(object):
    comments = db.ListField(db.EmbeddedDocumentField(Comment))


class Imaged(object):
    """TODO: IMplement ImageField"""
    pass


class Channel(db.DynamicDocument, Publishable, Slugged):
    name = db.StringField(max_length=255, required=True)
    description = db.StringField()
    show_in_menu = db.BooleanField(default=False)
    is_homepage = db.BooleanField(default=False)
    include_in_rss = db.BooleanField(default=False)
    indexable = db.BooleanField(default=True)
    canonical_url = db.StringField()
    order = db.IntField(default=0)

    # MPTT
    parent = db.ReferenceField('self')
    parent_slug = db.StringField(max_length=255)
    parent_long_slug = db.StringField(max_length=255)
    mpath = db.StringField()
    long_slug = db.StringField()

    def __unicode__(self):
        return "{}-{}".format(self.name, self.long_slug)


class Channeling(object):
    channel = db.ReferenceField(Channel, required=True)
    # Objects can be in only one main channel it gives an url
    # but the objects can also be relates to other channels
    channels = db.ListField(db.ReferenceField('Channel'))


###############################################################
# Base Content for every new content to extend. inheritance=True
###############################################################

class Content(db.DynamicDocument, Publishable, Slugged, Commentable, Channeling):
    title = db.StringField(max_length=255, required=True)

    def get_absolute_url(self):
        return url_for(self.URL_NAMESPACE, slug=self.slug)

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

admin.register(Channel)
