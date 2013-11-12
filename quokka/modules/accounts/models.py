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


class User(db.DynamicDocument, UserMixin):
    name = db.StringField(max_length=255)
    email = db.EmailField(max_length=255, unique=True)
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

    username = db.StringField(max_length=50, required=False, unique=True)

    def clean(self, *args, **kwargs):
        if not self.username:
            self.username = User.generate_username(self.email)

        try:
            super(User, self).clean(*args, **kwargs)
        except:
            pass

    @classmethod
    def generate_username(cls, email):
        username = email.lower()
        for item in ['@', '.', '-', '+']:
            username = username.replace(item, '_')
        return username

    def set_password(self, password, save=False):
        self.password = encrypt_password(password)
        if save:
            self.save()

    @classmethod
    def createuser(cls, name, email, password,
                   active=True, roles=None, username=None):

        username = username or cls.generate_username(email)
        return cls.objects.create(
            name=name,
            email=email,
            password=encrypt_password(password),
            active=active,
            roles=roles,
            username=username
        )

    def __unicode__(self):
        return "{0} <{1}>".format(self.name or '', self.email)
