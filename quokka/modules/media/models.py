# coding: utf-8

from quokka.core.db import db
from quokka.core.models import Content


class Media(Content):
    path = db.StringField()
    embed = db.StringField()
    link = db.StringField()

    meta = {
        'allow_inheritance': True
    }


class Image(Media):
    pass


class File(Media):
    pass


class Video(Media):
    pass


class Audio(Media):
    pass
