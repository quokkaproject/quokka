from .content.models import make_model, Category


def configure(app):

    # add context processors
    @app.context_processor
    def app_theme_context():
        if app.theme_context.get('DISPLAY_RECENT_POSTS_ON_SIDEBAR'):
            app.theme_context['articles'] = [
                make_model(item)
                for item in app.db.article_set({'published': True})
            ]

        app.theme_context['pages'] = [
            make_model(item)
            for item in app.db.page_set({'published': True})
        ]
        # app.theme_context['PAGES']
        # app.theme_context['tags']

        # TODO: Split categories by `/` to get roots
        app.theme_context['categories'] = [
            (Category(cat), [])
            for cat in app.db.value_set(
                'index', 'category',
                filter={'published': True},
                sort=True
            )
        ]
        # app.theme_context['tag_cloud']
        return app.theme_context
