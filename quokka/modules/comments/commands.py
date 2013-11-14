# coding: utf-8

from flask.ext.script import Command, Option
from .models import Comment


class ListComment(Command):
    "prints a list of medias"

    command_name = 'list_medias'

    option_list = (
        Option('--title', '-t', dest='title'),
    )

    def run(self, title=None):

        comments = Comment.objects
        if title:
            comments = comments(title=title)

        for comment in comments:
            print(comment)
