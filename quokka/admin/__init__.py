import import_string
from flask_admin import Admin
from tinymongo import TinyMongoCollection

from .views import FileAdmin, IndexView, ModelView


class QuokkaAdmin(Admin):
    """Customizable admin"""
    registered = []

    def register(self, model, view=None, identifier=None, *args, **kwargs):
        """Register views in a simpler way
            admin.register(
                Link,
                LinkAdmin,
                category="Content",
                name="Link"
            )
        """
        _view = view or ModelView

        if not identifier:
            if isinstance(model, TinyMongoCollection):
                identifier = '.'.join(
                    (view.__module__, view.__name__, model.tablename)
                )
            else:
                identifier = '.'.join((model.__module__, model.name))

            if identifier not in self.registered:
                self.add_view(_view(model, *args, **kwargs))
                self.registered.append(identifier)

    def add_icon(self, endpoint, icon, text):
        self.app.config.setdefault('ADMIN_ICONS', []).append(
            [endpoint, icon, text]
        )

    def add_content_format():
        # TODO: load cutsom content formats and types
        raise NotImplementedError()


def create_admin(app=None):
    """Admin factory"""
    index_view = IndexView()
    return QuokkaAdmin(
        app,
        index_view=index_view,
        template_mode=app.config.get('FLASK_ADMIN_TEMPLATE_MODE')
    )


def configure_admin(app, admin=None):  # noqa
    """Configure admin extensions"""
    admin = admin or create_admin(app)

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


def configure_file_admin(app):
    for entry in app.config.get('FILE_ADMIN', []):
        try:
            app.admin.add_view(
                FileAdmin(
                    entry['path'],
                    entry['url'],
                    name=entry['name'],
                    category=entry['category'],
                    endpoint=entry['endpoint'],
                    editable_extensions=entry.get('editable_extensions')
                )
            )
        except Exception as e:
            app.logger.info(e)


def configure_extra_views(app):
    # adding extra views
    extra_views = app.config.get('ADMIN_EXTRA_VIEWS', [])
    for view in extra_views:
        app.admin.add_view(
            import_string(view['module'])(
                category=view.get('category'),
                name=view.get('name')
            )
        )
