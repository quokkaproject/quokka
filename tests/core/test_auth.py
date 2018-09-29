import mock
import click
import getpass
from flask import current_app, url_for, Markup
from flask_htmlbuilder.htmlbuilder import html
from quokka.admin.actions import UserProfileBlockAction
from quokka.admin.views import ModelView
from quokka.admin.forms import Form, fields, ValidationError, validators
from quokka.utils.text import slugify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_simplelogin import SimpleLogin, get_username
from quokka.core.auth import create_user

def test_create_user():
    pass


def test_class_UserForm():
    pass


def test_format_profile():
    pass

def test_class_UserView():
    pass

def test_validate_login():
    pass


def test_configure():
    pass


def test_configure_user_admin():
    pass


def test_get_current_user():
    pass

