import pytest
import mock
from quokka.utils.echo import green, lecho, red
from quokka.utils.project import (
    fetch_theme, fetch_modules,
    cookiecutter
)

def test_fetch_theme():
    assert fetch_theme(theme="theme-mock", destiny="destiny-mock") is None

def test_fetch_modules():
    assert fetch_modules(modules="quokka", destiny="destiny-mock") is None

def test_cookiecutter():
    assert cookiecutter() is None

