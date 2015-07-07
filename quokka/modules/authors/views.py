#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.views import MethodView
from quokka.core.templates import render_template
from .utils import get_authors, get_author, get_author_contents


class AuthorListView(MethodView):
    """
    Show a full list of authors
    """

    def get(self):
        return render_template('authors/list.html', authors=get_authors())


class AuthorView(MethodView):
    """
    Show specific author profile
    """

    def get(self, author_id):
        author = get_author(author_id)
        contents = get_author_contents(author)
        return render_template('authors/detail.html',
                               author=author, contents=contents)
