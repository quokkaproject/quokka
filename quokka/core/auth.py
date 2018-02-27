import getpass
from flask import current_app
from quokka.admin.views import ModelView
from quokka.admin.forms import Form, fields, ValidationError
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
    username = fields.StringField(
        'Username',
        description='used as login'
    )
    fullname = fields.StringField(
        'Full Name',
        description='shows in author page'
    )
    email = fields.StringField('Email')
    password = fields.PasswordField(
        'Password',
        description=(
            "For new users provide a password. <br>"
            "For existing users provide for change. <br>"
            "or leave blank to keep existing password. <br>"
        )
    )


class UserView(ModelView):
    column_list = ('username', 'email')
    column_sortable_list = ('username', 'email')

    form = UserForm

    page_size = 20
    can_set_page_size = True

    def on_form_prefill(self, form, id):
        # username cannot be changed
        form.username.render_kw = {'readonly': True}

    # Correct user_id reference before saving
    def on_model_change(self, form, model, is_created):
        username = model.get('username')
        password = model.get('password')

        if is_created:
            # if password is blank raise error
            if not password:
                raise ValidationError('Password is required for new users')
            # new user so hash the new password
            model['_id'] = username
            model['password'] = generate_password_hash(
                password, method='pbkdf2:sha256'
            )
        else:
            # existing user, so compare if password is provided and changed
            current = current_app.db.users.find_one({'username': username})
            if password and current.get('password') != password:
                # if a different password provided, hash it
                model['password'] = generate_password_hash(
                    password, method='pbkdf2:sha256'
                )
            else:
                # if password is blank in form, keep the current
                model['password'] = current['password']

        model.pop('csrf_token', None)
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
        app.admin.add_icon(
            endpoint='quokka.core.auth.usersview.create_view',
            icon='glyphicon-user',
            text='New<br>User'
        )


def get_current_user():
    return get_username() or getpass.getuser()
