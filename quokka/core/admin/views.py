# Create customized index view class

from flask.ext import superadmin
from .models import Roled


class IndexView(Roled, superadmin.AdminIndexView):
    roles_accepted = ('admin', 'editor', 'moderator', 'writer', 'staff')
