# coding: utf-8

import datetime
from flask import current_app, request
from quokka.core.models import Content
from quokka.modules.accounts.models import User, Role


def get_author_contents(author):
    now = datetime.datetime.now()
    contents = Content.objects.filter(
        created_by=author,
        published=True,
        available_at__lte=now
    )
    if current_app.config.get("PAGINATION_ENABLED", True):
        pagination_arg = current_app.config.get("PAGINATION_ARG", "page")
        page = request.args.get(pagination_arg, 1)
        per_page = (
            request.args.get('per_page') or
            current_app.config.get("PAGINATION_PER_PAGE", 10)
        )
        contents = contents.paginate(page=int(page),
                                     per_page=int(per_page))
    return contents


def get_authors(*args, **kwargs):
    authors = User.objects.filter(
        roles__in=Role.objects.filter(
            name__in=['admin', 'author'],
            **kwargs
        )
    )
    if current_app.config.get("AUTHORS_PAGINATION_ENABLED", True):
        # FIXME: Error when above is False
        pagination_arg = current_app.config.get("PAGINATION_ARG", "page")
        page = request.args.get(pagination_arg, 1)
        per_page = (
            request.args.get('per_page') or
            current_app.config.get("AUTHORS_PAGINATION_PER_PAGE", 20)
        )
        authors = authors.paginate(page=int(page),
                                   per_page=int(per_page))
    return authors


def get_author(author_id):
    try:
        author = User.objects.get(id=author_id)
    except:
        author = User.objects.get(username=author_id)
    return author
