#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.security.utils import encrypt_password


# Auth
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    @classmethod
    def createrole(cls, name, description=None):
        return cls.objects.create(
            name=name,
            description=description
        )

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.description or 'Role')


class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(
        db.ReferenceField(Role, reverse_delete_rule=db.DENY), default=[]
    )

    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField(max_length=255)
    current_login_ip = db.StringField(max_length=255)
    login_count = db.IntField()

    @classmethod
    def createuser(cls, name, email, password, active=True, roles=None):
        return cls.objects.create(
            name=name,
            email=email,
            password=encrypt_password(password),
            active=active,
            roles=roles
        )

    def __unicode__(self):
        return "{0} <{1}>".format(self.name or '', self.email)
