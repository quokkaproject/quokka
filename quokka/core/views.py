# coding: utf-8

import logging
from datetime import datetime
from flask import request, redirect, render_template, url_for
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from quokka.core.models import Channel, Content, Comment

logger = logging.getLogger()


class ContentList(MethodView):

    def get(self, long_slug):
        now = datetime.now()
        path = long_slug.split('/')
        mpath = ",".join(path)
        mpath = ",{},".format(mpath)

        channel = Channel.objects.get_or_404(mpath=mpath)

        if not channel.is_homepage:
            contents = Content.objects(
                __raw__={'mpath': {'$regex': mpath}},
                published=True,
                available_at__lte=now,
                show_on_channel=True
            )
        else:
            contents = Content.objects(
                published=True,
                available_at__lte=now,
                show_on_channel=True
            )

        return render_template('content/list.html', contents=contents)


class ContentDetail(MethodView):
    form = model_form(
        Comment,
        exclude=['created_at', 'created_by',
                 'published', 'updated_at', 'last_updated_by']
    )

    def get_context(self, long_slug):
        now = datetime.now()
        homepage = Channel.objects.get(is_homepage=True)
        if long_slug.startswith(homepage.slug):
            slug = long_slug.split('/')[-1]
            return redirect(url_for('.detail', long_slug=slug))

        try:
            content = Content.objects.get(
                long_slug=long_slug,
                published=True,
                available_at__lte=now
            )
        except Content.DoesNotExist:
            content = Content.objects.get_or_404(
                channel=homepage,
                slug=long_slug,
                available_at__lte=now,
                published=True
            )

        form = self.form(request.form)

        context = {
            "content": content,
            "form": form
        }
        return context

    def get(self, long_slug):
        context = self.get_context(long_slug)
        if callable(context):
            return context
        return render_template('content/detail.html', **context)

    def post(self, long_slug):
        context = self.get_context(long_slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            content = context.get('content')
            content.comments.append(comment)
            content.save()

            return redirect(url_for('.detail', long_slug=long_slug))

        return render_template('content/detail.html', **context)


class ContentFeed(MethodView):
    pass


class ChannelFeed(ContentFeed):
    pass
