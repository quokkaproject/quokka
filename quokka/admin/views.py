# Create customized index view class

from flask import current_app, flash
from flask_admin.actions import action
# from quokka.core.models.content import Content
from quokka.utils.routing import expose
from .widgets import TextEditor, PrepopulatedText
from .utils import _, _l
from .ajax import AjaxModelLoader
from .models import (
    BaseIndexView,
    BaseView,
    ModelAdmin,
    BaseContentAdmin,
    ContentActions,
    PublishActions
)


class IndexView(BaseIndexView):
    roles_accepted = ('admin', 'editor', 'moderator', 'writer', 'staff',
                      'author')

    @expose('/')
    def index(self):
        return self.render('admin/index.html')


