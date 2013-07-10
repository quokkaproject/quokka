# coding : utf -8

from flask.ext.superadmin import model
from .models import Post
from quokka import admin


class PostAdmin(model.ModelAdmin):
    list_display = ('title', 'slug')


admin.register(Post, PostAdmin)
