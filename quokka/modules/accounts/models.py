#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from random import randint
from flask import url_for
from quokka.core.db import db
from quokka.core.models.custom_values import HasCustomValue
from quokka.utils.text import abbreviate, slugify
from flask_security import UserMixin, RoleMixin
from flask_security.utils import encrypt_password
from flask_gravatar import Gravatar
from .utils import ThemeChanger


logger = logging.getLogger()


# Auth
class Role(db.Document, ThemeChanger, HasCustomValue, RoleMixin):

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


class UserLink(db.EmbeddedDocument):
    title = db.StringField(max_length=50, required=True)
    link = db.StringField(max_length=255, required=True)
    icon = db.StringField(max_length=255)
    css_class = db.StringField(max_length=50)
    order = db.IntField(default=0)

    def __unicode__(self):
        return u"{0} - {1}".format(self.title, self.link)


class User(db.DynamicDocument, ThemeChanger, HasCustomValue, UserMixin):
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
    links = db.ListField(db.EmbeddedDocumentField(UserLink))

    use_avatar_from = db.StringField(
        choices=(
            ("gravatar", "gravatar"),
            ("url", "url"),
            ("upload", "upload"),
            ("facebook", "facebook")
        ),
        default='gravatar'
    )
    gravatar_email = db.EmailField(max_length=255)
    avatar_file_path = db.StringField()
    avatar_url = db.StringField(max_length=255)

    def get_avatar_url(self, *args, **kwargs):
        if self.use_avatar_from == 'url':
            return self.avatar_url
        elif self.use_avatar_from == 'upload':
            return url_for(
                'quokka.core.media', filename=self.avatar_file_path
            )
        elif self.use_avatar_from == 'facebook':
            try:
                return Connection.objects(
                    provider_id='facebook',
                    user_id=self.id,
                ).first().image_url
            except Exception as e:
                logger.warning(
                    '%s use_avatar_from is set to facebook but: Error: %s' % (
                        self.display_name, str(e)
                    )
                )
        return Gravatar()(
            self.get_gravatar_email(), *args, **kwargs
        )

    @property
    def summary(self):
        return (self.bio or self.tagline or '')[:255]

    def get_gravatar_email(self):
        return self.gravatar_email or self.email

    def clean(self, *args, **kwargs):
        if not self.username:
            self.username = User.generate_username(self.name)
        super(User, self).clean(*args, **kwargs)

    @classmethod
    def generate_username(cls, name, user=None):
        name = name or ''
        username = slugify(name)
        filters = {"username": username}
        if user:
            filters["id__ne"] = user.id
        if cls.objects.filter(**filters).count():
            username = "{0}{1}".format(username, randint(1, 1000))
        return username

    def set_password(self, password, save=False):
        self.password = encrypt_password(password)
        if save:
            self.save()

    @classmethod
    def createuser(cls, name, email, password,
                   active=True, roles=None, username=None,
                   *args, **kwargs):

        username = username or cls.generate_username(name)
        if 'links' in kwargs:
            kwargs['links'] = [UserLink(**link) for link in kwargs['links']]

        return cls.objects.create(
            name=name,
            email=email,
            password=encrypt_password(password),
            active=active,
            roles=roles,
            username=username,
            *args,
            **kwargs
        )

    @property
    def display_name(self):
        return abbreviate(self.name) or self.email

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
