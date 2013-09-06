# coding: utf-8

from flask.ext.script import (Command, Option, prompt,
                              prompt_pass, prompt_choices)
from .models import User, Role


class CreateRole(Command):
    "Create a role"

    command_name = "createrole"

    option_list = (
        Option('--name', '-n', dest='name'),
        Option('--description', '-d', dest='description'),

    )

    def run(self, name=None, description=None):
        if not name:
            name = prompt("Role Name")

        if not description:
            description = prompt("Role description")

        if all([name, description]):
            role = Role.objects.create(
                name=name,
                description=description
            )
        else:
            role = "Cant create the role"

        print(role)


class CreateSuperUser(Command):
    "Create a supersuer"

    command_name = 'createsuperuser'

    option_list = (
        Option('--name', '-n', dest='name'),
        Option('--email', '-e', dest='email'),
        Option('--password', '-p', dest='password'),
    )

    def run(self, name=None, email=None, password=None):
        if not name:
            name = prompt("Full Name")

        if not email:
            email = prompt("A valid email address")

        if not password:
            password = prompt_pass("Password")

        if all([name, email, password]):
            admin, created = Role.objects.get_or_create(name='admin')
            user = User.createuser(name, email, password, roles=[admin])
        else:
            user = "Cant create the supersuser"

        print(user)


class CreateUser(Command):
    "Create a user"

    command_name = 'createuser'

    option_list = (
        Option('--name', '-n', dest='name'),
        Option('--email', '-e', dest='email'),
        Option('--password', '-p', dest='password'),
        Option('--role', '-r', dest='role'),
    )

    def run(self, name=None, email=None, password=None, role=None):
        if not name:
            name = prompt("Full Name")

        if not email:
            email = prompt("A valid email address")

        if not password:
            password = prompt_pass("Password")

        if not role:
            roles = [r.name for r in Role.objects]
            role_name = prompt_choices("Role", choices=roles,
                                       no_choice=('none', ''))
            if role_name:
                role, created = Role.objects.get_or_create(name=role_name)
            else:
                role = None
        else:
            role, created = Role.objects.get_or_create(name=role)

        if all([name, email, password]):
            user = User.createuser(name, email, password, roles=[role])
        else:
            user = "Cant create the user"

        print(user)
