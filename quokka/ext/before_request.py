# coding: utf-8


def configure(app):
    @app.before_first_request
    def initialize():
        print "Called only once, when the first request comes in"
