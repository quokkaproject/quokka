# -*- coding: utf-8 -*-
import click
from ..models import Comment


@click.command()
@click.option('--title', default=None, help='Comment title')
def cli(title=None):
    "Prints a list of comments"

    comments = Comment.objects
    if title:
        comments = comments(title=title)

    for comment in comments:
        click.echo(comment)
