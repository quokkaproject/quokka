#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
from flask.ext.superadmin import Admin
from flask.ext.superadmin.contrib import fileadmin


def file_admin_factory(name):
    return type(name.capitalize(), (fileadmin.FileAdmin,), {})


def create_admin(app):

    SUPER_ADMIN = app.config.get(
        'SUPER_ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    admin = Admin(app, **SUPER_ADMIN)

    # EXCEPTION: UndefinedError: 'flask_superadmin.
    # contrib.fileadmin.FileAdmin object' has no attribute 'field_name'
    for entry in app.config.get('FILE_ADMIN', []):
        admin.add_view(
            file_admin_factory(entry['name'])(
                entry['path'],
                entry['url'],
                name=entry['name'],
                category=entry['category']
            )
        )

    return admin
