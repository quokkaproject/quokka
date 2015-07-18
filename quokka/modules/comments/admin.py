# coding : utf -8


from quokka import admin
from quokka.core.admin.models import ModelAdmin
from quokka.core.widgets import TextEditor
from .models import Comment
from quokka.utils.translation import _l


class CommentAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'moderator')
    column_list = ('path', 'author_name', 'author_email',
                   'created_at', 'published')
    form_columns = ['path', 'author_email', 'author_name',
                    'content_format', 'body', 'replies',
                    'created_at', 'created_by', 'published']
    form_args = {
        'body': {'widget': TextEditor()}
    }


admin.register(Comment, CommentAdmin, category=_l('Content'),
               name=_l("Comments"))
