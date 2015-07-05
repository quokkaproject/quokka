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
        return u"{0} ({1})".format(self.name, self.description or 'Role')


class UserLinks(db.EmbeddedDocument):
    title = db.StringField(max_length=50, required=True)
    link = db.StringField(max_length=255, required=True)
    icon = db.StringField(max_length=255)
    css_class = db.StringField(max_length=50)
    order = db.IntField(default=0)


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

    remember_token = db.StringField(max_length=255)
    authentication_token = db.StringField(max_length=255)

    tagline = db.StringField(max_length=255)
    bio = db.StringField()
    links = db.ListField(db.EmbeddedDocumentField(UserLinks))

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

    @property
    def display_name(self):
        return self.name or self.email

    def __unicode__(self):
        return u"{0} <{1}>".format(self.name or '', self.email)

    @property
    def connections(self):
        return Connection.objects(user_id=str(self.id))


class Connection(db.Document):
    user_id = db.ObjectIdField()
    provider_id = db.StringField(max_length=255)
    provider_user_id = db.StringField(max_length=255)
    access_token = db.StringField(max_length=255)
    secret = db.StringField(max_length=255)
    display_name = db.StringField(max_length=255)
    full_name = db.StringField(max_length=255)
    profile_url = db.StringField(max_length=512)
    image_url = db.StringField(max_length=512)
    rank = db.IntField(default=1)

    @property
    def user(self):
        return User.objects(id=self.user_id).first()