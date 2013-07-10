#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask.ext.superadmin import Admin


def create_admin(app):

    SUPER_ADMIN = app.config.get(
        'SUPER_ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    admin = Admin(app, **SUPER_ADMIN)

    # from quokka.blueprints.posts.models import Post
    # admin.register(Post)

    # from quokka.blueprints.posts.admin import register
    # register(admin)

    return admin
