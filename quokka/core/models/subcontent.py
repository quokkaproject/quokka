#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import url_for
from quokka.core.db import db
from quokka.utils.text import slugify
from quokka.core.models.signature import Publishable, Ordered

logger = logging.getLogger()


class SubContentPurpose(db.Document):
    title = db.StringField(max_length=255, required=True)
    identifier = db.StringField(max_length=255, required=True, unique=True)
    module = db.StringField()

    def save(self, *args, **kwargs):
        self.identifier = slugify(self.identifier or self.title)
        super(SubContentPurpose, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class SubContent(Publishable, Ordered, db.EmbeddedDocument):
    """Content can have inner contents
    Its useful for any kind of relation with Content childs
    Images, ImageGalleries, RelatedContent, Attachments, Media
    """

    content = db.ReferenceField('Content', required=True)
    caption = db.StringField()
    purpose = db.ReferenceField(SubContentPurpose, required=True)
    identifier = db.StringField()

    @property
    def thumb(self):
        try:
            return url_for('media', filename=self.content.thumb)
            # return self.content.thumb
        except Exception as e:
            logger.warning(str(e))
            return self.content.get_main_image_url(thumb=True)

    meta = {
        'ordering': ['order'],
        'indexes': ['order']
    }

    def clean(self):
        self.identifier = self.purpose.identifier

    def __unicode__(self):
        return self.content and self.content.title or self.caption
