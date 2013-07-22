# coding : utf -8
from quokka import admin
from quokka.core.admin.models import ModelAdmin
from .models import Role, User


class UserAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'email', 'active',
                   'last_login_at', 'login_count')


class RoleAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'description')


admin.register(User, UserAdmin, category="Accounts")
admin.register(Role, RoleAdmin, category="Accounts")
