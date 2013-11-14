# coding : utf -8

from quokka import admin
from quokka.core.admin.models import BaseContentAdmin
from quokka.core.widgets import TextEditor, PrepopulatedText
from quokka.core.admin import _, _l
from .models import Post


class PostAdmin(BaseContentAdmin):

    column_searchable_list = ('title', 'body', 'summary')

    form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
                    'body', 'published', 'contents',
                    'show_on_channel', 'available_at', 'available_until',
                    'tags', 'values', 'template_type']

    form_args = {
        'body': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }


admin.register(Post, PostAdmin, category=_("Content"), name=_l("Post"))
