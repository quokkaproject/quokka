# coding : utf -8
from quokka import admin

from .models import Role, User

admin.register(Role, category='accounts')
admin.register(User, category='accounts')
