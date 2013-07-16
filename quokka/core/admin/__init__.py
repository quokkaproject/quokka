#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask.ext.superadmin import Admin
from flask.ext.superadmin.contrib import fileadmin
from .views import IndexView


def create_admin(app=None):
    return Admin(index_view=IndexView())


def configure_admin(app, admin):

    SUPER_ADMIN = app.config.get(
        'SUPER_ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    for k, v in SUPER_ADMIN.items():
        setattr(admin, k, v)

    # admin.init_app(app)

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

    admin.init_app(app)
    return admin
