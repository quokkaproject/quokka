#!/usr/bin/env python
# -*- coding: utf-8 -*

import logging
from werkzeug.utils import import_string
from flask import request, session
from flask.ext.admin import Admin

from ..models import (Link, Config, SubContentPurpose, ChannelType,
                      ContentTemplateType, Channel)

from .models import ModelAdmin, FileAdmin, BaseIndexView
from .views import (IndexView, InspectorView, LinkAdmin, ConfigAdmin,
                    SubContentPurposeAdmin, ChannelTypeAdmin,
                    ContentTemplateTypeAdmin, ChannelAdmin)

from quokka.utils.translation import _l, _n

'''
_n is here only for backwards compatibility, to be imported by 3rd party
modules. The below _n below is to avoid pep8 error
'''
_n  # noqa

logger = logging.getLogger()


class QuokkaAdmin(Admin):
    def register(self, model, view=None, *args, **kwargs):
        _view = view or ModelAdmin
        self.add_view(_view(model, *args, **kwargs))
        # try:
        #     self.add_view(_view(model, *args, **kwargs))
        # except Exception as e:
        #     logger.warning(
        #         "admin.register({0}, {1}, {2}, {3}) error: {4}".format(
        #             model, view, args, kwargs, e.message
        #         )
        #     )


def create_admin(app=None):
    index_view = IndexView()
    return QuokkaAdmin(app, index_view=index_view)


def configure_admin(app, admin):  # noqa

    custom_index = app.config.get('ADMIN_INDEX_VIEW')
    if custom_index:
        admin.index_view = import_string(custom_index)()
        if isinstance(admin._views[0], BaseIndexView):
            del admin._views[0]
        admin._views.insert(0, admin.index_view)

    admin_config = app.config.get(
        'ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    for k, v in list(admin_config.items()):
        setattr(admin, k, v)

    babel = app.extensions.get('babel')
    if babel:
        try:
            @babel.localeselector
            def get_locale():
                # use default language if set
                if app.config.get('BABEL_DEFAULT_LOCALE'):
                    session['lang'] = app.config.get('BABEL_DEFAULT_LOCALE')
                else:
                    # get best matching language
                    if app.config.get('BABEL_LANGUAGES'):
                        session['lang'] = request.accept_languages.best_match(
                            app.config.get('BABEL_LANGUAGES')
                        )

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
                    name=_l(entry['name']),
                    category=_l(entry['category']),
                    endpoint=entry['endpoint'],
                    roles_accepted=entry.get('roles_accepted'),
                    editable_extensions=entry.get('editable_extensions')
                )
            )
        except Exception as e:
            logger.info(e)
            #  need to check blueprint endpoisnt colision

    # register all themes in file manager
    for k, theme in app.theme_manager.themes.items():
        try:

            if k == app.config.get('DEFAULT_THEME'):
                suffix = "(Site theme)"
            elif k == app.config.get('ADMIN_THEME'):
                suffix = "(Admin theme)"
            else:
                suffix = "Theme"

            admin.add_view(
                FileAdmin(
                    theme.static_path,
                    "/_themes/{0}/".format(theme.identifier),
                    name="{0}: {1} static files".format(suffix,
                                                        theme.identifier),
                    category=_l("Files"),
                    endpoint="{0}_static_files".format(theme.identifier),
                    roles_accepted=('admin', "editor"),
                    editable_extensions=app.config.get(
                        'DEFAULT_EDITABLE_EXTENSIONS')
                )
            )
            admin.add_view(
                FileAdmin(
                    theme.templates_path,
                    "/theme_template_files/{0}/".format(theme.identifier),
                    name="{0}: {1} template files".format(suffix,
                                                          theme.identifier),
                    category=_l("Files"),
                    endpoint="{0}_template_files".format(theme.identifier),
                    roles_accepted=('admin', "editor"),
                    editable_extensions=app.config.get(
                        'DEFAULT_EDITABLE_EXTENSIONS')
                )
            )
        except:
            pass

    # adding views
    admin.add_view(InspectorView(category=_l("Settings"),
                                 name=_l("Inspector")))

    # adding extra views
    extra_views = app.config.get('ADMIN_EXTRA_VIEWS', [])
    for view in extra_views:
        admin.add_view(
            import_string(view['module'])(
                category=_l(view.get('category')),
                name=_l(view.get('name'))
            )
        )

    # adding model views
    admin.register(
        Link,
        LinkAdmin,
        category=_l("Content"),
        name=_l("Link")
    )
    admin.register(Config,
                   ConfigAdmin,
                   category=_l("Settings"),
                   name=_l("Config"))
    admin.register(SubContentPurpose,
                   SubContentPurposeAdmin,
                   category=_l("Settings"),
                   name=_l("Sub content purposes"))
    admin.register(ChannelType, ChannelTypeAdmin,
                   category=_l("Settings"), name=_l("Channel type"))
    admin.register(ContentTemplateType,
                   ContentTemplateTypeAdmin,
                   category=_l("Settings"),
                   name=_l("Template type"))
    admin.register(Channel, ChannelAdmin,
                   category=_l("Content"), name=_l("Channel"))

    # avoid registering twice
    if admin.app is None:
        admin.init_app(app)

    return admin
