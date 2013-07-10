#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka import app
from flask.ext.mongoengine import MongoEngine
db = MongoEngine(app)
