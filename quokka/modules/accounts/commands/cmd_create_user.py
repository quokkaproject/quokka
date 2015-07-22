# -*- coding: utf-8 -*-
import click
from ..models import User, Role


@click.command()
@click.option('--name', help='Full Name', prompt=True)
@click.option('--email', help='Email', prompt=True)
@click.option('--password', help='Password', prompt=True, hide_input=True,
              confirmation_prompt=True)
@click.option('--role', help='Role', prompt=True)
def cli(name=None, email=None, password=None, role=None):
    "Create a user"

    role, created = Role.objects.get_or_create(name=role)

    if all([name, email, password]):
        user = User.createuser(name, email, password, roles=[role])
    else:
        user = "Cant create the user"

    click.echo(user)
