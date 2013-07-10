#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask.ext.superadmin import Admin


def create_admin(app):
    from quokka.blueprints.posts.models import Post
    SUPER_ADMIN = app.config.get('SUPER_ADMIN', {'title': 'Quokka Admin'})
    title = SUPER_ADMIN.get('title')
    admin = Admin(app, title)
    admin.register(Post)
