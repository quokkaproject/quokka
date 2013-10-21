# coding: utf-8

from flask.ext.script import Command, Option
from .models import Media


class ListMedia(Command):
    "prints a list of medias"

    command_name = 'list_medias'

    option_list = (
        Option('--title', '-t', dest='title'),
    )

    def run(self, title=None):

        medias = Media.objects
        if title:
            medias = medias(title=title)

        for media in medias:
            print(media)
