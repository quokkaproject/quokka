# coding : utf -8
from wtforms.fields import TextField
from wtforms.widgets import PasswordInput
from quokka import admin
from quokka.core.admin import _, _l
from quokka.core.admin.models import ModelAdmin
from .models import Role, User


class UserAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'email', 'active',
                   'last_login_at', 'login_count')
    form_columns = ('name', 'email', 'roles', 'active', 'newpassword',
                    'confirmed_at',
                    'last_login_at', 'current_login_at', 'last_login_ip',
                    'current_login_ip', 'login_count')

    form_extra_fields = {
        "newpassword": TextField(widget=PasswordInput())
    }

    def on_model_change(self, form, model, is_created):
        if model.newpassword:
            model.set_password(model.newpassword, save=True)


class RoleAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'description')


admin.register(User, UserAdmin, category=_("Accounts"), name=_l("User"))
admin.register(Role, RoleAdmin, category=_("Accounts", name=_l("Roles")))
