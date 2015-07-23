# -*- coding: utf-8 -*-
import click
from ..models import Media


@click.command()
@click.option('--title', default=None, help='Filter by file name')
def cli(title):
    'Prints a list of medias'

    medias = Media.objects
    if title:
        medias = medias(title=title)

    for media in medias:
        click.echo(media)
