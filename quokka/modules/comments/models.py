# coding: utf-8
import uuid
from quokka.core.db import db
from quokka.core.models import Publishable


class BaseComment(object):
    author_name = db.StringField(max_length=255, required=True)
    author_email = db.StringField(max_length=255)
    body = db.StringField(required=True)
    spam = db.BooleanField()
    deleted = db.BooleanField()

    @property
    def gravatar_email(self):
        if self.created_by:
            return self.created_by.email
        return self.author_email


class Reply(Publishable, BaseComment, db.EmbeddedDocument):
    uid = db.StringField()
    parent = db.StringField()

    def clean(self):
        if not self.uid:
            self.uid = str(uuid.uuid4())


class Comment(Publishable, BaseComment, db.Document):
    path = db.StringField(max_length=255, required=True)
    replies = db.ListField(db.EmbeddedDocumentField(Reply))

    def __unicode__(self):
        return u"{0} - {1}...".format(self.author_name, self.body[:15])

    meta = {
        "ordering": ['-created_at'],
        "indexes": ['-created_at', 'path']
    }
