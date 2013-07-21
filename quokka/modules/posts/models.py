#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from quokka.core.models import Content


class Post(Content):
    # URL_NAMESPACE = 'posts.detail'
    body = db.StringField(required=True)
