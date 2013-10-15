#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.app import QuokkaModule

module = QuokkaModule('posts', __name__, template_folder='templates')

# Register the urls if needed
# in this case there is no need to register any specific url
# from .views import ListView, DetailView
# module.add_url_rule('/posts/', view_func=ListView.as_view('list'))
# module.add_url_rule('/posts/<slug>/', view_func=DetailView.as_view('detail'))
