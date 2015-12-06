# coding: utf-8

from quokka.core.app import QuokkaModule
module = QuokkaModule("media", __name__, template_folder="templates")

# Register the urls if needed
# from .views import ListView, DetailView
# module.add_url_rule('/media/', view_func=ListView.as_view('list'))
# module.add_url_rule('/media/<slug>/', view_func=DetailView.as_view('detail'))
