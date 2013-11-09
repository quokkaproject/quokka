#!/usr/bin/env python
# -*- coding: utf-8 -*

import logging

from flask import request, session
from flask.ext.admin import Admin

from ..models import (Link, Config, SubContentPurpose, ChannelType,
                      ContentTemplateType, Channel)

from .models import ModelAdmin, FileAdmin
from .views import (IndexView, InspectorView, LinkAdmin, ConfigAdmin,
                    SubContentPurposeAdmin, ChannelTypeAdmin,
                    ContentTemplateTypeAdmin, ChannelAdmin)

from .utils import _, _l

logger = logging.getLogger()


class QuokkaAdmin(Admin):
    def register(self, model, view=None, *args, **kwargs):
        View = view or ModelAdmin
        self.add_view(View(model, *args, **kwargs))
        # try:
        #     self.add_view(View(model, *args, **kwargs))
        # except Exception as e:
        #     logger.warning(
        #         "admin.register({0}, {1}, {2}, {3}) error: {4}".format(
        #             model, view, args, kwargs, e.message
        #         )
        #     )


def create_admin(app=None):
    return QuokkaAdmin(app, index_view=IndexView())


def configure_admin(app, admin):

    ADMIN = app.config.get(
        'ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    for k, v in list(ADMIN.items()):
        setattr(admin, k, v)

    babel = app.extensions.get('babel')
    if babel:
        try:
            @babel.localeselector
            def get_locale():
                override = request.args.get('lang')

                if override:
                    session['lang'] = override

                return session.get('lang', 'en')
            admin.locale_selector(get_locale)
        except:
            pass  # Exception: Can not add locale_selector second time.

    for entry in app.config.get('FILE_ADMIN', []):
        try:
            admin.add_view(
                FileAdmin(
                    entry['path'],
                    entry['url'],
                    name=entry['name'],
                    category=entry['category'],
                    endpoint=entry['endpoint']
                )
            )
        except:
            pass  # TODO: check blueprint endpoisnt colision

    # adding views
    admin.add_view(InspectorView(category=_("Settings"),
                                 name=_l("Inspector")))

    # adding model views
    admin.register(
        Link,
        LinkAdmin,
        category=_("Content"),
        name=_l("Link")
    )
    admin.register(Config,
                   ConfigAdmin,
                   category=_("Settings"),
                   name=_l("Config"))
    admin.register(SubContentPurpose,
                   SubContentPurposeAdmin,
                   category=_("Settings"),
                   name=_l("Sub content purposes"))
    admin.register(ChannelType, ChannelTypeAdmin,
                   category=_("Settings"), name=_l("Channel type"))
    admin.register(ContentTemplateType,
                   ContentTemplateTypeAdmin,
                   category=_("Settings"),
                   name=_l("Template type"))
    admin.register(Channel, ChannelAdmin,
                   category=_("Content"), name=_l("Channel"))

    # avoind registering twice
    if admin.app is None:
        admin.init_app(app)

    return admin
