import mock
import click
from flask import render_template
from flask import current_app as app
from flask.views import MethodView
from quokka.core.content.models import make_model
from quokka.core.views.sitemap import SiteMapView


#######################################################
#pytest - fixtures                                    #
#######################################################
sitemapview = SiteMapView()


#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_class_sitemapview_isinstance():
    assert isinstance(sitemapview, SiteMapView) is True

def test_class_sitemap_decorators_empty_tuple():
    assert sitemapview.decorators == ()

def test_class_sitemap_mehots_dicionary_GET():    
    assert  sitemapview.methods == {'GET'}

def test_class_sitemap_provide_automatic_options_property_is_None():
    assert sitemapview.provide_automatic_options is None


