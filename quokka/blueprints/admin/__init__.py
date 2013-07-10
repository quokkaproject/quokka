#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from .views import List, Detail

module = Blueprint('admin', __name__, template_folder='templates')


# Register the urls
module.add_url_rule('/admin/', view_func=List.as_view('index'))
module.add_url_rule('/admin/create/', defaults={'slug': None},
                    view_func=Detail.as_view('create'))
module.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
