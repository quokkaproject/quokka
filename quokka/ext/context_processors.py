# coding: utf-8

import datetime
from quokka.core.models import Channel


def configure(app):

    @app.context_processor
    def inject_channels():
        now = datetime.datetime.now()
        return dict(channels=Channel.objects(published=True,
                                             available_at__lte=now))
