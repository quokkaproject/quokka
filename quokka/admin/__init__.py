#!/usr/bin/env python
# -*- coding: utf-8 -*
import import_string

from flask_admin import Admin

from quokka.utils.translation import _l

from tinymongo import TinyMongoCollection

from .views import ModelView, FileAdmin, IndexView

from quokka.config import settings


class QuokkaAdmin(Admin):
    """Customizable admin"""
    registered = []

    def register(self, model, view=None, identifier=None, *args, **kwargs):
        """Register views in a simpler way
            admin.register(
                Link,
                LinkAdmin,
                category=_l("Content"),
                name=_l("Link")
            )
        """
        _view = view or ModelView

        if not identifier:
            if isinstance(model, TinyMongoCollection):
                identifier = '.'.join(
                    (view.__module__, view.__name__, model.tablename)
                )
            else:
                identifier = '.'.join((model.__module__, model.__name__))

            if identifier not in self.registered:
                self.add_view(_view(model, *args, **kwargs))
                self.registered.append(identifier)


def create_admin(app=None):
    """Admin factory"""
    index_view = IndexView()
    return QuokkaAdmin(
        app,
        index_view=index_view,
        template_mode=settings.get('FLASK_ADMIN_TEMPLATE_MODE')
    )


def configure_admin(app, admin):  # noqa
    """Configure admin extensions"""

    custom_index = app.config.get('ADMIN_INDEX_VIEW')
    if custom_index:
        admin.index_view = import_string(custom_index)()
        if isinstance(admin._views[0], IndexView):  # noqa
            del admin._views[0]  # noqa
        admin._views.insert(0, admin.index_view)  # noqa

    admin_config = app.config.get(
        'ADMIN',
        {
            'name': 'Quokka Admin',
            'url': '/admin'
        }
    )

    for key, value in list(admin_config.items()):
        setattr(admin, key, value)

    # avoid registering twice
    if admin.app is None:
        admin.init_app(app)

    return admin


def configure_file_admin(app, admin):
    for entry in app.config.get('FILE_ADMIN', []):
        try:
            admin.add_view(
                FileAdmin(
                    entry['path'],
                    entry['url'],
                    name=_l(entry['name']),
                    category=_l(entry['category']),
                    endpoint=entry['endpoint'],
                    editable_extensions=entry.get('editable_extensions')
                )
            )
        except Exception as e:
            app.logger.info(e)


def configure_extra_views(app, admin):
    # adding extra views
    extra_views = app.config.get('ADMIN_EXTRA_VIEWS', [])
    for view in extra_views:
        admin.add_view(
            import_string(view['module'])(
                category=_l(view.get('category')),
                name=_l(view.get('name'))
            )
        )
