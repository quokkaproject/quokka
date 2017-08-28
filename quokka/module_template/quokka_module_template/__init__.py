from .admin import UserView, TweetView


def configure(app):
    app.admin.register(
        app.db.users,
        UserView,
        # category='User',
        name='User'
    )

    app.admin.register(
        app.db.get_collection('tweets'),
        TweetView,
        # category='User',
        name='Tweets'
    )
