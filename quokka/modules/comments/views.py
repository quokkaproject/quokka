#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from flask.ext.security import current_user
from quokka.core.templates import render_template
from .models import Comment


class CommentView(MethodView):

    form = model_form(
        Comment,
        only=['author_name', 'author_email', 'body']
    )

    def render_context(self, path, form):
        comments = Comment.objects(path=path, published=True)
        return render_template('content/comments.html',
                               comments=comments,
                               form=form,
                               path=path)

    def get(self, path):
        return self.render_context(path, form=self.form())

    def post(self, path):
        form = self.form(request.form)

        if form.validate():
            comment = Comment(path=path)
            form.populate_obj(comment)
            if current_user.is_authenticated():
                # TODO: logic to auto publish comments
                comment.published = True
                comment.author_name = current_user.name
                comment.author_email = current_user.email
            comment.save()
            return self.render_context(path, form=self.form())

        return self.render_context(path, form=form)
