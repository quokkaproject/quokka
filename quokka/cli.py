# coding: utf-8
import errno
import shutil
import sys
from pathlib import Path
from pprint import pprint

import click
import yaml
from manage.cli import cli, init_cli
from manage.template import default_manage_dict
from quokka.core.auth import create_user
from quokka.core.errors import DuplicateKeyError
from . import create_app as App


@cli.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def runserver(reloader, debug, host, port):
    """Run the Flask development server i.e. app.run()"""
    App().run(
        use_reloader=reloader,
        debug=debug,
        host=host,
        port=port,
        extra_files=['settings.yml', '.secrets.yml']  # for reloader
    )


@cli.command()
def check():
    """Prints app status"""
    app = App()
    click.echo("Extensions.")
    pprint(app.extensions)
    click.echo("Modules.")
    pprint(app.blueprints)
    click.echo("App.")
    return app


@cli.command()
def showconfig():
    """click.echo all Quokka config variables"""
    from pprint import pprint
    click.echo("Config.")
    pprint(dict(App().config))


def copyfolder(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


@cli.command()
@click.argument('name', required=True)
@click.option('--destiny', required=False, default=None)
@click.option('--source', required=False, default=None)
@click.option('--theme', required=False, default=None)
@click.option('--modules', required=False, default=None)
def init(name, destiny, source, theme, modules):
    """Initialize a new project in current folder\n
    $ quokka init mywebsite
    """
    folder_name = name.replace(' ', '_').lower()

    if destiny is None:
        destiny = f'./{folder_name}'
    else:
        destiny = f'{destiny}/{folder_name}'

    source = source or Path.joinpath(
        Path(sys.modules['quokka'].__file__).parent,
        'project_template'
    )

    copyfolder(source, destiny)
    # TODO: fetch theme
    # TODO: fetch and install modules

    with open(f'{destiny}/manage.yml', 'w') as manage_file:
        data = default_manage_dict
        data['project_name'] = name.title()
        manage_file.write(yaml.dump(data, default_flow_style=False))


@cli.command()
@click.option('--username', required=True, prompt=True)
@click.option('--email', required=False, default=None, prompt=True)
@click.option('--password', required=True, prompt=True, hide_input=True,
              confirmation_prompt=True)
def adduser(username, email, password):
    """Add new user with admin access"""
    app = App()
    with app.app_context():
        try:
            create_user(username=username, password=password, email=email)
        except DuplicateKeyError as e:
            click.echo(str(e).replace('_id', 'username'))
        else:
            click.echo(
                'User {0} created!!! go to: {1}'.format(username, '/admin')
            )


def main():
    """
    Quokka CMS command line manager
    overwrites the manage loader
    """
    manager = init_cli(cli)
    # TODO: implement locked: to avoid manage to run
    return manager()  # from quokka.utils.populate import Populate
