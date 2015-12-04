#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from quokka.core.models.content import Content


class Post(Content):
    # URL_NAMESPACE = 'posts.detail'
    body = db.StringField(required=True)
