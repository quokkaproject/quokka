#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from .views import ListView, DetailView

module = Blueprint('posts', __name__, template_folder='templates')

# Register the urls
module.add_url_rule('/', view_func=ListView.as_view('list'))
module.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
