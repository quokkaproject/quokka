# -*- coding: utf-8 -*-
import click
from ..models import Role


@click.command()
@click.option('--name', help='Role name', prompt=True)
@click.option('--description', help='Role description', prompt=True)
def cli(name, description):
    "Create a role"

    if all([name, description]):
        role = Role.createrole(
            name=name,
            description=description
        )
    else:
        role = "Cant create the role"

    click.echo(role)
