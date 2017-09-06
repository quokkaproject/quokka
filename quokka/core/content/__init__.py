from .admin import ContentView


def configure(app):
    # Register admin views
    app.admin.register(
        app.db.index,
        ContentView,
        name='Content',
        endpoint='contentview'
    )

    # Admin admin index panel icons
    app.admin.add_icon(
        endpoint='quokka.core.content.admin.contentview.create_view',
        icon='glyphicon-file',
        text='New<br>Content'
    )

    app.admin.add_icon(
        endpoint='quokka.core.content.admin.contentview.index_view',
        icon='glyphicon-list',
        text='All<br>Content'
    )

    # Register new commands

    # Register content types

    # Register content formats

    # should return an identifier string
    return 'content'
