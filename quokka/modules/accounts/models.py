#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from flask.ext.security import UserMixin, RoleMixin


# Auth
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.description or 'Role')


class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField(max_length=255)
    current_login_ip = db.StringField(max_length=255)
    login_count = db.IntField()

    def __unicode__(self):
        return u"{} <{}>".format(self.name or '', self.email)
