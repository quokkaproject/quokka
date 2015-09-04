# -*- coding: utf-8 -*-
import click
from pprint import pprint
from ..models import User, Role


@click.command()
def cli():
    "List all Roles and its members"
    for role in Role.objects:
        click.echo('_' * 20)
        click.echo(role.name)
        click.echo(
            pprint(
                [user for user in User.objects.filter(roles=role)]
            )
        )
