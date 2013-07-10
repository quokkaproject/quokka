#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask.ext.superadmin import Admin


def create_admin(app):
    from quokka.blueprints.posts.models import Post

    admin = Admin(app, 'Simple Models')
    admin.register(Post)
