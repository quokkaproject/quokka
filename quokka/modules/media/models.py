# coding: utf-8
import logging

from quokka.core.db import db
from quokka.core.models import Content, Channel
from flask.ext.admin import form
from .controller import MediaController

logger = logging.getLogger()


class Media(MediaController, Content):

    DEFAULT_CHANNEL = "media"

    path = db.StringField()
    embed = db.StringField()
    link = db.StringField()

    meta = {
        'allow_inheritance': True
    }

    @classmethod
    def get_default_channel(cls):
        default_channel = cls.DEFAULT_CHANNEL
        try:
            return Channel.objects.get(long_slug=default_channel)
        except Exception as e:
            logger.warning(str(e))
            return Channel.get_homepage()


class Image(Media):
    DEFAULT_CHANNEL = 'media/images'

    @property
    def thumb(self):
        return form.thumbgen_filename(self.path)


class File(Media):
    DEFAULT_CHANNEL = 'media/files'


class Video(Media):
    DEFAULT_CHANNEL = 'media/videos'


class Audio(Media):
    DEFAULT_CHANNEL = 'media/audios'


class MediaGallery(Content):
    body = db.StringField(required=False)
