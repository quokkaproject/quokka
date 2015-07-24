# -*- coding: utf-8 -*-
import click
import json
from pprint import pprint
from ..models import User


@click.command()
def cli():
    "List all Users"
    for user in User.objects:
        click.echo('_' * 20)
        click.echo(user.display_name)
        user_data = json.loads(user.to_json())
        del user_data['password']
        user_data['roles'] = user.roles
        click.echo(pprint(user_data))
