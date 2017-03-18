# coding: utf-8


def configure(app):
    """Left as example on how to add before request processor"""
    @app.before_first_request
    def initialize():
        app.logger.info("Called only once, when the first request comes in")
