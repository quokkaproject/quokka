#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import current_app
from quokka.core.db import db
from quokka.core.fields import MultipleObjectsReturned
from quokka.core.models.custom_values import HasCustomValue
from quokka.core.models.signature import (
    Publishable, ContentFormat, Dated, Slugged
)

logger = logging.getLogger()


class Config(HasCustomValue, ContentFormat, Publishable, db.DynamicDocument):
    group = db.StringField(max_length=255)
    description = db.StringField()

    @classmethod
    def get(cls, group, name=None, default=None):

        try:
            instance = cls.objects.get(group=group)
        except:
            return None

        if not name:
            ret = instance.values
            if group == 'settings':
                ret = {}
                ret.update(current_app.config)
                ret.update({item.name: item.value for item in instance.values})
        else:
            try:
                ret = instance.values.get(name=name).value
            except (MultipleObjectsReturned, AttributeError):
                ret = None

        if not ret and group == 'settings' and name is not None:
            # get direct from store to avoid infinite loop
            ret = current_app.config.store.get(name)

        return ret or default

    def __unicode__(self):
        return self.group


class Quokka(Dated, Slugged, db.DynamicDocument):
    """ Hidden collection for installation control"""
