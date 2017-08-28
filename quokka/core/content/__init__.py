from .admin import ContentView


def configure(app):
    app.admin.register(
        app.db.index,
        ContentView,
        name='Content',
        endpoint='contentview'
    )
    return 'content'
