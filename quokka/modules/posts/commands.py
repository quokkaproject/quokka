# coding: utf-8

from flask.ext.script import Command, Option
from .models import Post


class ListPosts(Command):
    "prints a list of posts"

    command_name = 'list_posts'

    option_list = (
        Option('--title', '-t', dest='title'),
    )

    def run(self, title=None):

        posts = Post.objects
        if title:
            posts = posts(title=title)

        for post in posts:
            print(post)
