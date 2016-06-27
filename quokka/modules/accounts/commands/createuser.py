# -*- coding: utf-8 -*-
import click
from quokka import create_app_base
from ..models import User, Role


app = create_app_base(ext_list=['quokka.ext.security.configure'])


def create_user(name=None, email=None, password=None, role=None):
    "Create a user"

    role, created = Role.objects.get_or_create(name=role)

    with app.app_context():
        if all([name, email, password]):
            user = User.createuser(name, email, password, roles=[role])
        else:
            user = "Cant create the user"

        click.echo(user)


@click.command()
@click.option('--name', help='Full Name', prompt=True)
@click.option('--email', help='Email', prompt=True)
@click.option('--password', help='Password', prompt=True, hide_input=True,
              confirmation_prompt=True)
@click.option('--role', help='Role', prompt=True)
def cli(name=None, email=None, password=None, role=None):
    "Create a user"
    create_user(name, email, password, role)
