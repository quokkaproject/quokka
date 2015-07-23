# -*- coding: utf-8 -*-
import click
from ..models import Post


@click.command()
@click.option('--title', default=None, help='Title of the Post')
def cli(title):
    "Prints a list of posts"

    posts = Post.objects
    if title:
        posts = posts(title=title)

    for post in posts:
        click.echo(post)
