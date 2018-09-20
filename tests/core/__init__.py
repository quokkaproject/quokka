import mock
import pytest
from quokka.core.app import QuokkaModule
from quokka.core.content.admin import AdminArticlesView, AdminPagesView, AdminBlocksView
from quokka.core.content.views import (
    DetailView, PreviewView, ArticleListView, CategoryListView, TagListView,
    AuthorListView
)
from quokka.core.content.utils import url_for_content, strftime
from quokka.core.content import configure
from quokka import create_app

#WIP:
"""
needs to see who use it
import mock
import pytest
from quokka.core.app import QuokkaModule
from quokka.core.content.admin import AdminArticlesView, AdminPagesView, AdminBlocksView
from quokka.core.content.views import (
    DetailView, PreviewView, ArticleListView, CategoryListView, TagListView,
    AuthorListView
)
from quokka.core.content.utils import url_for_content, strftime
from quokka.core.content import configure
from quokka import create_app
from quokka.core.content import configure


"""
def test_configure():
    pass








