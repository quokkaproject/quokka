import click
from quokka import create_app

app = create_app()

@click.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def runserver(reloader, debug, host, port):
    """Run the Flask development server i.e. app.run()"""
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)
