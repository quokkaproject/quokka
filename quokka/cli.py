# coding: utf-8
import errno
import shutil
import sys
from functools import wraps
from pathlib import Path
from pprint import pprint

import click
import manage
from manage.cli import cli, init_cli

from . import create_app
from .core.auth import create_user
from .core.errors import DuplicateKeyError
from .utils.echo import b, blue, green, lecho, red, yellow
from .utils.project import cookiecutter, fetch_modules, fetch_theme

CWD = Path.cwd()
QUOKKA_ROOT_FOLDER = Path(sys.modules['quokka'].__file__).parent

# TODO: https://github.com/ryukinix/decorating
# TODO: https://github.com/click-contrib/click-completion


def with_app(f):
    """Calls function passing app as first argument"""
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            app = create_app(ENVMODE=kwargs.get('envmode'))
        except IOError as e:
            click.echo(
                'Quokka project not found, run `quokka init [projectname] [.]`'
                ' to start a new project or ensure `./quokka.yml` exists. '
                f'Error: {e}'
            )
            return
        return f(app=app, *args, **kwargs)
    return decorator


@cli.command()
@click.option('--reloader/--no-reloader', default=None)
@click.option('--debug/--no-debug', default=None)
@click.option('--host', default=None)
@click.option('--port', default=None)
@click.option('--envmode', default=None)
@with_app
def runserver(app=None, reloader=None, debug=None,
              host=None, port=None, envmode=None):
    """Run the Flask development server i.e. app.run()"""
    debug = debug or app.config.get('DEBUG', False)
    reloader = reloader or app.config.get('RELOADER', False)
    host = host or app.config.get('HOST', '127.0.0.1')
    port = port or app.config.get('PORT', 5000)

    app.run(
        use_reloader=reloader,
        debug=debug,
        host=host,
        port=port,
        extra_files=['quokka.yml', '.secrets.yml']  # for reloader
    )


@cli.command()
@with_app
def check(app=None):
    """Prints app status"""
    click.echo("Extensions.")
    pprint(app.extensions)
    click.echo("Modules.")
    pprint(app.blueprints)
    click.echo("App.")
    return app


def copyfolder(src, dst):
    try:
        shutil.copytree(src, dst)
    except FileExistsError as exc:
        lecho('Warning', exc, red)
        sys.exit(1)
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
    destiny_folder = Path(name.replace(' ', '_').lower())
    project_template = QUOKKA_ROOT_FOLDER / Path('project_template')

    if destiny is None:
        destiny = CWD / destiny_folder
    elif destiny in ('.', './'):
        destiny = CWD
    else:
        destiny = Path(destiny) / destiny_folder

    source = source or project_template

    # Copy project template from quokka root
    copyfolder(source, destiny)
    click.echo(
        b('🐹  Quokka project created 🐹')
    )
    lecho('📝  Name', name, green)
    lecho('📁  Location', destiny, green)
    if source == project_template:
        lecho('📚  Template', 'default', green)
    else:
        lecho('📚  Template', source, green)

    # Fetch themes and extensions
    fetch_theme(theme, destiny)
    fetch_modules(modules, destiny)

    # Rewrite the config file
    cookiecutter(
        destiny,
        name=name,
        theme=theme,
        modules=modules,
        source=source
    )

    click.echo(blue(f'➡ Go to {destiny}'))
    click.echo(blue('⚙  Run `quokka runserver` to start!'))
    click.echo(blue('📄  Check the documentation on http://quokkaproject.org'))
    click.echo(yellow('🐹  Happy Quokka! 🐹'))


@cli.command()
@click.option('--username', required=True, prompt=True)
@click.option('--email', required=False, default=None, prompt=True)
@click.option('--password', required=True, prompt=True, hide_input=True,
              confirmation_prompt=True)
@with_app
def adduser(app, username, email, password):
    """Add new user with admin access"""
    with app.app_context():
        try:
            create_user(username=username, password=password, email=email)
        except DuplicateKeyError as e:
            click.echo(str(e).replace('_id', 'username'))
        else:
            click.echo(
                'User {0} created!!! go to: {1}'.format(username, '/admin')
            )


# TODO:
# update - updates current project settings and assets to latest version


@cli.command()
@click.argument('line', required=True)
@with_app
def execute(app, line):
    """Execute arbitrary command line in app context and outputs result"""
    with app.app_context():
        click.echo(eval(line, {'app': app}))


def main():
    """
    Quokka CMS command line manager
    overwrites the `manage` loader
    """
    manage.cli.MANAGE_FILE = 'quokka.yml'
    manager = init_cli(cli)
    return manager()


if __name__ == "__main__":
    main()
