import pytest
import mock
from functools import partial
import click
from quokka.utils.echo import lecho

################################
#pytest - fixtures - setUp();  #
################################
b = partial(click.style, bold=True)
blue = partial(click.style, bold=True, fg="blue")
green = partial(click.style, bold=True, fg="green")
red = partial(click.style, bold=True, fg="red")
yellow = partial(click.style, bold=True, fg="yellow")
modules = "quokka"


#################################
#pytest - Quokka - test_cli.py  #
#################################
def test_lecho():
    assert lecho('Modules installed', modules, green) is None

 
