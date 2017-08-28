# coding: utf-8

from flask import current_app
from quokka.admin.views import ModelView
from quokka.admin.forms import Form, fields
from werkzeug.security import check_password_hash, generate_password_hash
from flask_simplelogin import SimpleLogin


def create_user(**data):
    if 'username' not in data or 'password' not in data:
        raise ValueError('username and password are required.')

    data['_id'] = data['username']
    data['password'] = generate_password_hash(
        data.pop('password'),
        method='pbkdf2:sha256'
    )
    current_app.db.users.insert_one(data)
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
    db_user = current_app.db.users.find_one({"_id": user['username']})
    if not db_user:
        return False
    if check_password_hash(db_user['password'], user['password']):
        return True
    return False


def configure(app):
    SimpleLogin(app, login_checker=validate_login)


def configure_user_admin(app):
    app.admin.register(
        app.db.users,
        UserView,
        name='Users',
        category='Administration'
    )
