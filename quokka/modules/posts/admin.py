# coding : utf -8
from quokka import admin
from flask.ext.superadmin import model
from quokka.core.admin.models import Roled

from .models import Post


class PostAdmin(Roled, model.ModelAdmin):
    roles_accepted = ('admin', 'editor')
    list_display = ('title', 'slug')


admin.register(Post, PostAdmin, category="content")
