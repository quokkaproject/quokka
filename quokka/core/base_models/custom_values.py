#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from quokka.core.db import db
from quokka.core.admin.utils import _l


def default_formatter(value):
    return value


class CustomValue(db.EmbeddedDocument):

    FORMATS = (
        ('json', "json"),
        ('text', "text"),
        ('int', "int"),
        ('float', "float"),
    )

    DEFAULT_FORMATTER = default_formatter

    FORMATTERS = {
        'json': json.loads,
        'text': DEFAULT_FORMATTER,
        'int': int,
        'float': float
    }

    REVERSE_FORMATTERS = {
        'json': lambda val: val if isinstance(val, str) else json.dumps(val),
        'text': DEFAULT_FORMATTER,
        'int': DEFAULT_FORMATTER,
        'float': DEFAULT_FORMATTER
    }

    name = db.StringField(max_length=50, required=True)
    rawvalue = db.StringField(verbose_name=_l("Value"),
                              required=True)
    formatter = db.StringField(choices=FORMATS, default="text", required=True)

    @property
    def value(self):
        return self.FORMATTERS.get(self.formatter,
                                   self.DEFAULT_FORMATTER)(self.rawvalue)

    @value.setter
    def value(self, value):
        self.rawvalue = self.REVERSE_FORMATTERS.get(self.formatter,
                                                    self.STR_FORMATTER)(value)

    def clean(self):
        try:
            self.value
        except Exception as e:
            # raise base exception because Flask-Admin can't handle the output
            # for some specific Exceptions of Mongoengine
            raise Exception(e.message)
        super(CustomValue, self).clean()

    def __unicode__(self):
        return u"{s.name} -> {s.value}".format(s=self)


class HasCustomValue(object):
    values = db.ListField(db.EmbeddedDocumentField(CustomValue))

    def get_values_tuple(self):
        return [(value.name, value.value, value.formatter)
                for value in self.values]

    def get_value(self, name, default=None):
        try:
            return self.values.get(name=name).value
        except:
            return default

    def clean(self):
        current_names = [value.name for value in self.values]
        for name in current_names:
            if current_names.count(name) > 1:
                raise Exception(_l("%(name)s already exists",
                                   name=name))
        super(HasCustomValue, self).clean()
