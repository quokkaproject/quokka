# -*- coding: utf-8 -*-
import click
from .createuser import create_user


@click.command()
@click.option('--name', help='Full name', prompt=True)
@click.option('--email', help='A valid email address', prompt=True)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def cli(name, email, password):
    """Create a user with administrator permissions"""
    create_user(name, email, password, 'admin')
