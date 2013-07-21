# Create customized index view class

from quokka.utils.routing import expose
from .models import BaseIndexView


class IndexView(BaseIndexView):
    roles_accepted = ('admin', 'editor', 'moderator', 'writer', 'staff')

    @expose('/')
    def index(self):
        return self.render('admin/index.html')
