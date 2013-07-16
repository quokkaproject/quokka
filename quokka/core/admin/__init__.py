#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask.ext.superadmin import Admin
from flask.ext.superadmin.contrib import fileadmin
from .views import IndexView


def create_admin(app):

    SUPER_ADMIN = app.config.get(
        'SUPER_ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    admin = Admin(app, index_view=IndexView(), **SUPER_ADMIN)

    babel = app.extensions.get('babel')
    if babel:
        admin.locale_selector(babel.localeselector)

    for entry in app.config.get('FILE_ADMIN', []):
        admin.add_view(
            fileadmin.FileAdmin(
                entry['path'],
                entry['url'],
                name=entry['name'],
                category=entry['category'],
                endpoint=entry['name']
            )
        )

    return admin
