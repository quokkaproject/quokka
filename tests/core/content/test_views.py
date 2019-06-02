import pytest
import mock
import click
import hashlib
import PyRSS2Gen as pyrss
from datetime import (
    datetime, timedelta
)
from flask import (
    current_app as app, render_template,
    abort, request
)
from flask.views import MethodView
from flask_simplelogin import is_logged_in
from quokka.utils.atom import AtomFeed
from quokka.core.content.models import (
    make_model, make_paginator,
    Category, Tag, Author
)
from quokka.utils.text import (
    slugify_category, normalize_var,
    slugify, cdata, make_external_url
)
from quokka.core.content.views import (
    BaseView, ArticleListView,
    CategoryListView, TagListView,
    AuthorListView, DetailView,
    PreviewView
)


#######################################################
#pytest - fixtures                                    #
#######################################################
baseview = BaseView()
articlelistview = ArticleListView()
categorylistview = CategoryListView()
taglistview = TagListView()
authorlistview = AuthorListView()
detailview = DetailView()
previewview = PreviewView()


#######################################################
#pytest - Quokka - tests/core/content/test_views.py   #
#######################################################
def test_class_baseview_is_subclass():
    assert issubclass(BaseView, MethodView) == True

def test_class_baseview_is_instance():
    assert isinstance(baseview, BaseView) == True

def test_class_baseview_decorators():
    assert baseview.decorators == ()

def test_class_baseview_methods():
    assert baseview.methods is None

def test_class_baseview_provide_automatic_options_property():
    assert baseview.provide_automatic_options is None

def test_class_articlelistview_is_subclass():
    assert issubclass(ArticleListView, BaseView) == True

def test_class_articlelistview_is_instance():
    assert isinstance(articlelistview, ArticleListView) == True

def test_class_articlelistview_decorators_property():
    assert articlelistview.decorators == ()

def test_class_articlelistview_methods_property():
    assert articlelistview.methods == {'GET'}

def test_class_articlelistview_provide_automatic_options_property():
    assert articlelistview.provide_automatic_options is None

def test_class_categorylistview_is_subclass():
    assert issubclass(CategoryListView, BaseView) == True

def test_class_categorylistview_is_instance():
    assert isinstance(categorylistview, CategoryListView) == True

def test_class_categorylistview_is_instance():
    assert categorylistview.decorators == ()

def test_class_categorylistview_methods_property():
    assert categorylistview.methods == {'GET'}

def test_class_categorylistview_provide_automatic_options():
    assert categorylistview.provide_automatic_options is None

def test_class_taglistview_is_subclass():
    assert issubclass(TagListView, BaseView) == True

def test_isinstance_TagListView_is_instance():
    assert isinstance(taglistview, TagListView) == True

def test_class_taglistview_decorators():
    assert taglistview.decorators == ()

def test_class_taglistview_methods_property():
    assert taglistview.methods == {'GET'}

def test_class_taglistview_provide_automatic_options():
    assert taglistview.provide_automatic_options is None

def test_class_authorlistview_is_subclass():
    assert issubclass(AuthorListView, BaseView) == True

def test_class_authorlistview_is_instance():
    assert isinstance(authorlistview, AuthorListView) == True

def test_class_authorlistview_decorators():
    assert authorlistview.decorators == ()

def test_class_authorlistview_methods_property():
    assert authorlistview.methods == {'GET'}

def test_class_authorlistview_provide_automatic_options():
    assert authorlistview.provide_automatic_options is None

def test_class_detailview_is_subclass():
    assert issubclass(DetailView, BaseView) == True

def test_class_detailview_is_instance():
    assert isinstance(detailview, DetailView) == True

def test_class_detailview_decorators():
    assert detailview.decorators == ()

def test_class_detailview_methods_property():
    assert detailview.methods == {'GET'}

def test_class_detailview_provide_automatic_options():
    assert detailview.provide_automatic_options is None

def test_class_detailview_is_preview():
    assert detailview.is_preview is False

def test_class_previewview_is_subclass():
    assert issubclass(PreviewView, DetailView) == True

def test_class_previewview_is_instance():
    assert isinstance(previewview, PreviewView) == True

def test_class_previewview_decorators():
    assert previewview.decorators == ()

def test_class_previewview_methods_property():
    assert previewview.methods == {'GET'}

def test_class_previewview_provide_automatic_options():
    assert previewview.provide_automatic_options is None

def test_class_previewview_is_preview():
    assert previewview.is_preview is True
