from flask.ext.security.forms import RegisterForm, Required
from flask.ext.security import Security as _Security
from flask.ext.security import MongoEngineUserDatastore
from wtforms import TextField
from quokka.modules.accounts.models import Role, User
from quokka.core.templates import render_template


class Security(_Security):
    def render_template(self, *args, **kwargs):
        return render_template(*args, **kwargs)


class ExtendedRegisterForm(RegisterForm):
    name = TextField('Name', [Required()])


def init_app(app, db):
    app.security = Security(app, MongoEngineUserDatastore(db, User, Role),
                            register_form=ExtendedRegisterForm,
                            confirm_register_form=ExtendedRegisterForm)
