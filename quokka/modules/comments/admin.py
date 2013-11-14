# coding : utf -8


from quokka import admin
from quokka.core.admin import _, _l
from quokka.core.admin.models import ModelAdmin
from .models import Comment


class CommentAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')
    column_list = ('path', 'author_name', 'author_email',
                   'created_at', 'published')
    form_columns = ['path', 'author_email', 'author_name', 'body', 'replies',
                    'created_at', 'created_by', 'published']


admin.register(Comment, CommentAdmin, category=_('Content'),
               name=_l("Comments"))
