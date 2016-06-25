#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine
from .fields import ListField

db = MongoEngine()
db.ListField = ListField
