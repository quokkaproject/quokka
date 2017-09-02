from functools import partial
import click

b = partial(click.style, bold=True)
blue = partial(click.style, bold=True, fg="blue")
green = partial(click.style, bold=True, fg="green")
red = partial(click.style, bold=True, fg="red")
yellow = partial(click.style, bold=True, fg="yellow")


def lecho(label, text, style=b):
    """Click.echo with label e.g: 'Name: Foo' """
    click.echo(f'{style(label.rstrip(":"))}: {text}')
