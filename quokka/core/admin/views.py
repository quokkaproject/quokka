# Create customized index view class

from flask.ext import superadmin
from .models import Roled


def expose(url='/', methods=('GET',)):
    """
        Use this decorator to expose views in your view classes.

        `url`
            Relative URL for the view
        `methods`
            Allowed HTTP methods. By default only GET is allowed.
    """
    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f

    return wrap


class IndexView(Roled, superadmin.AdminIndexView):
    roles_accepted = ('admin', 'editor', 'moderator', 'writer', 'staff')

    @expose('/')
    def index(self):
        return self.render('admin/index.html')
