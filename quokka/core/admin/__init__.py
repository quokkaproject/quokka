#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask.ext.admin import Admin
from flask.ext.admin.contrib import fileadmin
from .views import IndexView


def create_admin(app=None):
    return Admin(index_view=IndexView())


def configure_admin(app, admin):

    ADMIN = app.config.get(
        'ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    for k, v in ADMIN.items():
        setattr(admin, k, v)

    # babel = app.extensions.get('babel')
    # if babel:
    #     try:
    #         admin.locale_selector(babel.localeselector)
    #     except:
    #         pass  # Exception: Can not add locale_selector second time.

    for entry in app.config.get('FILE_ADMIN', []):
        try:
            admin.add_view(
                fileadmin.FileAdmin(
                    entry['path'],
                    entry['url'],
                    name=entry['name'],
                    category=entry['category'],
                    endpoint=entry['endpoint']
                )
            )
        except:
            pass  # TODO: check blueprint endpoisnt colision

    if admin.app is None:
        admin.init_app(app)

    return admin
