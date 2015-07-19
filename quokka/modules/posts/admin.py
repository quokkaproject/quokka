# coding : utf -8

from quokka import admin
from quokka.core.admin.models import BaseContentAdmin
from quokka.core.widgets import TextEditor, PrepopulatedText
from .models import Post
from quokka.utils.translation import _l


class PostAdmin(BaseContentAdmin):

    column_searchable_list = ('title', 'body', 'summary')

    form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
                    'content_format', 'body', 'authors',
                    'comments_enabled', 'published', 'add_image', 'contents',
                    'show_on_channel', 'available_at', 'available_until',
                    'tags', 'values', 'template_type', 'license']

    form_args = {
        'body': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }


admin.register(Post, PostAdmin, category=_l("Content"), name=_l("Post"))
