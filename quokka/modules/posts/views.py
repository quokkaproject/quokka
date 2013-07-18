#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, redirect, render_template, url_for
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from quokka.core.models import Comment
from .models import Post

import logging
logger = logging.getLogger()


class ListView(MethodView):

    def get(self):
        logger.info('getting list of posts')
        posts = Post.objects.exclude('comments').all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):

    form = model_form(
        Comment,
        exclude=['created_at', 'created_by',
                 'published', 'updated_at', 'last_updated_by']
    )

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)
