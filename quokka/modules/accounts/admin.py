# coding : utf -8
from wtforms.fields import TextField
from wtforms.widgets import PasswordInput
from quokka import admin
from quokka.core.admin.models import ModelAdmin
from .models import Role, User, Connection
from quokka.utils.translation import _l


class UserAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_searchable_list = ('name', 'email')
    column_list = ('name', 'email', 'active',
                   'last_login_at', 'login_count')
    form_columns = ('name', 'email', 'roles', 'active', 'newpassword',
                    'confirmed_at',
                    'last_login_at', 'current_login_at', 'last_login_ip',
                    'current_login_ip', 'login_count', 'tagline',
                    'bio', 'links', 'values')

    form_extra_fields = {
        "newpassword": TextField(widget=PasswordInput())
    }

    def on_model_change(self, form, model, is_created):
        if model.newpassword:
            setpwd = model.newpassword
            del model.newpassword
            model.set_password(setpwd, save=True)


class RoleAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'description', 'values')


class ConnectionAdmin(ModelAdmin):
    roles_accepted = ('admin',)


admin.register(User, UserAdmin, category=_l("Accounts"), name=_l("User"))
admin.register(Role, RoleAdmin, category=_l("Accounts"), name=_l("Roles"))
admin.register(Connection, ConnectionAdmin,
               category=_l("Accounts"), name=_l("Connection"))
