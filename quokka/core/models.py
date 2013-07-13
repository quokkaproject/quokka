#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import url_for
from quokka.core.db import db
from quokka import admin

#Channel


# Content
class Content(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    comments = db.ListField(db.ReferenceField('Comment'))

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


class Comment(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
    published = db.BooleanField(default=True)


admin.register(Comment, category="content")
