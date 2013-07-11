# coding : utf -8
from quokka import admin
from flask.ext.superadmin import model
from quokka.core.admin.models import Roled
from .models import Role, User


class UserAdmin(Roled, model.ModelAdmin):
    roles_accepted = ('admin',)
    list_display = ('name', 'email', 'active',
                    'last_login_at', 'login_count')


class RoleAdmin(Roled, model.ModelAdmin):
    roles_accepted = ('admin',)
    list_display = ('name', 'description')


admin.register(Role, RoleAdmin, category='accounts')
admin.register(User, UserAdmin, category='accounts')
