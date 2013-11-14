# coding: utf-8

from quokka.core.app import QuokkaModule
from .views import CommentView

module = QuokkaModule("comments", __name__, template_folder="templates")
module.add_url_rule('/comment/<path:path>/',
                    view_func=CommentView.as_view('comment'))
