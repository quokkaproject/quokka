# coding: utf-8
import logging
import click
import shutil
import errno
import yaml
from pprint import pprint
from manage.cli import create_shell, init_cli, cli
from manage.template import default_manage_dict
from quokka import create_app
from quokka.errors import DuplicateKeyError
from quokka.ext.security import User
# from quokka.utils.populate import Populate

app = create_app()


if app.config.get("LOGGER_ENABLED"):
    logging.basicConfig(
        level=getattr(logging, app.config.get("LOGGER_LEVEL", "DEBUG")),
        format=app.config.get(
            "LOGGER_FORMAT",
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
        datefmt=app.config.get("LOGGER_DATE_FORMAT", '%d.%m %H:%M:%S')
    )


@cli.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def runserver(reloader, debug, host, port):
    """Run the Flask development server i.e. app.run()"""
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)


@cli.command()
def check():
    """Prints app status"""
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
    pprint(dict(app.config))


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
def init(name):
    """Initialize a new project in current folder\n
    $ quokka init mywebsite
    """
    folder_name = name.replace(' ', '_').lower()
    destiny = './{0}'.format(folder_name)
    copyfolder(
        '/home/brocha/Projects/quokka_ng/quokka/project_template',
        destiny
    )
    with open('{0}/manage.yml'.format(destiny), 'w') as manage_file:
        data = default_manage_dict
        data['project_name'] = name.title()
        manage_file.write(yaml.dump(data, default_flow_style=False))


@cli.command()
@click.option('--username', required=True)
@click.option('--email', required=True)
@click.option('--password', required=True)
def adduser(username, email, password):
    """Add new user with admin access"""
    # TODO: improve click.options to password
    try:
        User.create(username, email, password)
    except DuplicateKeyError as e:
        click.echo(str(e).replace('_id', 'username'))
    else:
        # TODO: get app_url dynamically
        app_url = 'http://localhost:5000/admin'
        click.echo('User {0} created!!! go to: {1}'.format(username, app_url))


def main():
    """
    Quokka CMS command line manager
    overwrites the manage loader
    """
    manager = init_cli(cli)
    # TODO: implement locked: to avoid manage to run
    return manager()
