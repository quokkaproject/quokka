#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
from flask.ext.superadmin import Admin
from flask.ext.superadmin.contrib import fileadmin


def create_admin(app):

    SUPER_ADMIN = app.config.get(
        'SUPER_ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    admin = Admin(app, **SUPER_ADMIN)

    # TODO: Add multiple instances of fileadmin
    # EXCEPTION: UndefinedError: 'flask_superadmin.contrib.fileadmin.FileAdmin object' has no attribute 'field_name'
    # admin.add_view(fileadmin.FileAdmin(app.static_folder, '/staticfiles', name='Static'))
    admin.add_view(fileadmin.FileAdmin(
        os.path.join(app.config.get('PROJECT_ROOT'), app.template_folder),
        '/templatefiles',
        name='template_files')
    )

    return admin
