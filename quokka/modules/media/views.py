#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.views import MethodView
from quokka.core.templates import render_template

from .models import Media

import logging
logger = logging.getLogger()


class ListView(MethodView):

    def get(self):
        logger.info('getting list of media')
        medias = Media.objects.all()
        return render_template('media/list.html', medias=medias)


class DetailView(MethodView):

    def get_context(self, slug):
        media = Media.objects.get_or_404(slug=slug)

        context = {
            "media": media
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('medias/detail.html', **context)
