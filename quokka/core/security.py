# coding: utf-8

from flask_login import LoginManager
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, redirect, url_for, flash
from flask_login import login_user, logout_user, UserMixin
from quokka import db
from quokka.template import render_template
from quokka.admin.forms import Form, fields
from quokka.admin.views import ModelView


class User(UserMixin):

    def __init__(self, username, email=None):
        self.username = username
        self.email = email

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def create(username, email, password, hash_password=True):
        """Create a new user"""
        if hash_password is True:
            password = generate_password_hash(password, method='pbkdf2:sha256')

        data = {
            '_id': username,
            'username': username,
            'password': password,
            'email': email
        }
        db.users.insert_one(data)

        return get_user(username)


class LoginForm(Form):
    """Login form to access writing and settings pages"""

    username = fields.StringField('Username', validators=[DataRequired()])
    password = fields.PasswordField('Password', validators=[DataRequired()])


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
        return model


def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.users.find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj, remember=True)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("admin.index"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


def logout():
    logout_user()
    return redirect(url_for('quokka.login'))


def get_user(username):
    user = db.users.find_one({"_id": username})
    if not user:
        return None
    return User(user['_id'], user['email'])


def configure(app, db):
    lm = LoginManager(app)
    lm.login_view = 'quokka.login'
    lm.logout_view = 'quokka.logout'
    lm.user_callback = get_user
    # lm.localize_callback = # babel_gettext

    app.add_quokka_url_rule(
        '/login/', view_func=login, methods=['GET', 'POST'], endpoint='login'
    )

    app.add_quokka_url_rule(
        '/logout/', view_func=logout, endpoint='logout'
    )


def configure_user_admin(app, db, admin):
    admin.register(
        db.users,
        UserView,
        name='Users',
        category='Administration'
    )
