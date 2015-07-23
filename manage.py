#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import click
from quokka import create_app
from quokka.ext.blueprints import blueprint_commands
from quokka.core.db import db

app = create_app()

if app.config.get("LOGGER_ENABLED"):
    logging.basicConfig(
        level=getattr(logging, app.config.get("LOGGER_LEVEL", "DEBUG")),
        format=app.config.get(
            "LOGGER_FORMAT",
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
        datefmt=app.config.get("LOGGER_DATE_FORMAT", '%d.%m %H:%M:%S')
    )


@click.group()
def core_cmd():
    """ Core commands """
    pass


@core_cmd.command()
@click.option('--ipython/--no-ipython', default=True)
def shell(ipython):
    """Runs a Python shell with Quokka context"""
    import code
    import readline
    import rlcompleter
    _vars = globals()
    _vars.update(locals())
    _vars.update(dict(app=app, db=db))
    readline.set_completer(rlcompleter.Completer(_vars).complete)
    readline.parse_and_bind("tab: complete")
    try:
        if ipython is True:
            from IPython import start_ipython
            start_ipython(argv=[], user_ns=_vars)
        else:
            raise ImportError
    except ImportError:
        shell = code.InteractiveConsole(_vars)
        shell.interact()


@core_cmd.command()
def check():
    """Prints app status"""
    from pprint import pprint
    print("Extensions.")
    pprint(app.extensions)
    print("Modules.")
    pprint(app.blueprints)
    print("App.")
    return app


@core_cmd.command()
@click.option(
    '--f',
    help='Fixtures JSON path',
    default='./etc/fixtures/initial_data.json')
def populate(f):
    """Populate the database with sample data"""
    from quokka.utils.populate import Populate
    Populate(db, filepath=f)()


@core_cmd.command()
def showconfig():
    """Print all config variables"""
    from pprint import pprint
    print("Config.")
    pprint(dict(app.config))


@core_cmd.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def runserver(reloader, host, port):
    """Run the Flask development server i.e. app.run()"""
    app.run(use_reloader=reloader, host=host, port=port)

help_text = """
    Subcommands are loaded from the modules/commands folder dynamically.
    The file must be called cmd_<command_name> with a function 'cli'
    being the click.command to be loaded:

    Example:

    \b
    import click
    @click.command()
    def cli():
        click.echo("Do whatever you want")
    """
manager = click.CommandCollection(help=help_text)
manager.add_source(core_cmd)
manager.add_source(blueprint_commands(app))

if __name__ == '__main__':
    with app.app_context():
        manager()
