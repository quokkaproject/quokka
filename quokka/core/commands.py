# coding: utf-8
import logging
import click
from pprint import pprint
from manage.cli import create_shell
from quokka import create_app
from quokka.core.db import db
from quokka.utils.populate import Populate

app = create_app()


if app.config.get("LOGGER_ENABLED"):
    logging.basicConfig(
        level=getattr(logging, app.config.get("LOGGER_LEVEL", "DEBUG")),
        format=app.config.get(
            "LOGGER_FORMAT",
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
        datefmt=app.config.get("LOGGER_DATE_FORMAT", '%d.%m %H:%M:%S')
    )


@click.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def runserver(reloader, debug, host, port):
    """Run the Flask development server i.e. app.run()"""
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)


@click.command()
def check():
    """Prints app status"""
    click.echo("Extensions.")
    pprint(app.extensions)
    click.echo("Modules.")
    pprint(app.blueprints)
    click.echo("App.")
    return app


@click.command()
@click.option(
    '-f',
    '--filename',
    help='Fixtures JSON path',
    default='./etc/fixtures/initial_data.json')
@click.option('-b', '--baseurl', help='base url to use', default=None)
@click.option('--reset/--no-reset', default=False)
def populate(filename, baseurl=None, reset=False):
    """Populate the database with sample data"""
    populator = Populate(db, filepath=filename, baseurl=baseurl, app=app)
    if not reset:
        try:
            populator()
        except RuntimeError:
            with app.test_request_context(
                    base_url=baseurl or 'http://localhost:5000/'):
                populator()
    else:
        populator.reset()


@click.command()
def showconfig():
    """click.echo all Quokka config variables"""
    from pprint import pprint
    click.echo("Config.")
    pprint(dict(app.config.store))


@click.command()
@click.option('console', '--ipython', default=True, flag_value='ipython',
              help='Start with ipython console')
@click.option('console', '--ptpython', flag_value='ptpython',
              help='Start with ptpython console')
@click.option('console', '--bpython', flag_value='bpython',
              help='Start with bpython console')
@click.option('console', '--python', flag_value='python',
              help='Start with python console')
def shell(console):
    """Runs a Python shell with Quokka context"""
    context = {'app': app, 'db': db}
    return create_shell(console, extra_vars=context)
