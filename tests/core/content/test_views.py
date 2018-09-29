import mock
import click
import hashlib
import PyRSS2Gen as pyrss
from datetime import datetime, timedelta
from flask import current_app as app, render_template, abort, request
from flask.views import MethodView
from flask_simplelogin import is_logged_in
from quokka.utils.atom import AtomFeed
from .models import make_model, make_paginator, Category, Tag, Author
from quokka.utils.text import (
    slugify_category, normalize_var, slugify, cdata, make_external_url
)
from quokka.core.content.views import BaseView 

def test_class_BaseView():
    pass


def test_class_ArticleListView():
    pass


def test_class_CategoryListView():
    pass


def test_class_TagListView():
    pass


def test_class_AuthorListView():
    pass


def test_class_DetailView():
    pass


def test_class_PreviewView():
    pass


