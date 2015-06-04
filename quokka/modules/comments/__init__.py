# coding: utf-8

from quokka.core.app import QuokkaModule
from .views import CommentView
from .models import Comment


module = QuokkaModule("comments", __name__, template_folder="templates")
module.add_url_rule('/comment/<path:path>/',
                    view_func=CommentView.as_view('comment'))


def get_comment(**kwargs):
    try:
        return Comment.objects.get(**kwargs)
    except:
        return None


def get_comments(limit=None, order_by="-created_at", **kwargs):
    contents = Comment.objects.filter(**kwargs).order_by(order_by)
    if limit:
        contents = contents[:limit]
    return contents


module.add_app_template_global(get_comment)
module.add_app_template_global(get_comments)
