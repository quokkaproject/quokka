# coding: utf-8

from quokka.core.app import QuokkaModule
from .views import AuthorListView, AuthorView
from .utils import get_author, get_authors, get_author_contents


module = QuokkaModule("authors", __name__, template_folder="templates")
module.add_url_rule('/author/<author_id>/',
                    view_func=AuthorView.as_view('author'))
module.add_url_rule('/authors/',
                    view_func=AuthorListView.as_view('authors'))
module.add_app_template_global(get_author)
module.add_app_template_global(get_authors)
module.add_app_template_global(get_author_contents)
