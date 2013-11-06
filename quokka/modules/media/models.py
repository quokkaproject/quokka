# coding: utf-8

from quokka.core.db import db
from quokka.core.models import Content
from flask.ext.admin import form
from .controller import MediaController


class Media(MediaController, Content):
    path = db.StringField()
    embed = db.StringField()
    link = db.StringField()

    meta = {
        'allow_inheritance': True
    }


class Image(Media):
    @property
    def thumb(self):
        return form.thumbgen_filename(self.path)


class File(Media):
    pass


class Video(Media):
    pass


class Audio(Media):
    pass


class MediaGallery(Content):
    body = db.StringField(required=False)
