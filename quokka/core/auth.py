import getpass
from flask import current_app
from quokka.admin.views import ModelView
from quokka.admin.forms import Form, fields
from werkzeug.security import check_password_hash, generate_password_hash
from flask_simplelogin import SimpleLogin, get_username


def create_user(**data):
    if 'username' not in data or 'password' not in data:
        raise ValueError('username and password are required.')

    data['_id'] = data['username']
    data['password'] = generate_password_hash(
        data.pop('password'),
        method='pbkdf2:sha256'
    )
    # current_app.db.users.insert_one(data)
    current_app.db.insert('users', data)
    return data


class UserForm(Form):
    username = fields.StringField('Username')
    email = fields.StringField('Email')
    password = fields.PasswordField('Password')


class UserView(ModelView):
    column_list = ('username', 'email')
    column_sortable_list = ('username', 'email')

    form = UserForm

    page_size = 20
    can_set_page_size = True

    # Correct user_id reference before saving
    def on_model_change(self, form, model):
        model['_id'] = model.get('username')
        # todo reencrypt password if changed
        return model


def validate_login(user):
    # db_user = current_app.db.users.find_one({"_id": user['username']})
    db_user = current_app.db.get('users', {"_id": user['username']})
    if not db_user:
        return False
    if check_password_hash(db_user['password'], user['password']):
        return True
    return False


def configure(app):
    if app.config.get('ADMIN_REQUIRES_LOGIN') is True:
        SimpleLogin(app, login_checker=validate_login)


def configure_user_admin(app):
    if app.config.get('ADMIN_REQUIRES_LOGIN') is True:
        app.admin.register(
            app.db.users,
            UserView,
            name='Users',
            category='Administration'
        )


def get_current_user():
    return get_username() or getpass.getuser()
