# coding : utf -8
from quokka import admin
from quokka.core.admin import _, _l
from quokka.core.admin.models import ModelAdmin
from .models import Role, User


class UserAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'email', 'active',
                   'last_login_at', 'login_count')
    form_columns = ('name', 'email', 'roles', 'active', 'confirmed_at',
                    'last_login_at', 'current_login_at', 'last_login_ip',
                    'current_login_ip', 'login_count')


class RoleAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'description')


admin.register(User, UserAdmin, category=_("Accounts"), name=_l("User"))
admin.register(Role, RoleAdmin, category=_("Accounts", name=_l("Roles")))
