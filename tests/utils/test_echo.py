import pytest
import mock
from functools import partial
import click


################################
#pytest - fixtures - setUp();  #
################################
b = partial(click.style, bold=True)
blue = partial(click.style, bold=True, fg="blue")
green = partial(click.style, bold=True, fg="green")
red = partial(click.style, bold=True, fg="red")
yellow = partial(click.style, bold=True, fg="yellow")


#################################
#pytest - Quokka - test_cli.py  #
#################################
def test_lecho():
    pass
 
