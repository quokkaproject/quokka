

def configure(app):

    # add context processors
    @app.context_processor
    def app_theme_context():
        return app.theme_context
