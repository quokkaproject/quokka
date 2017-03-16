# coding: utf-8

from flask_login import LoginManager
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, redirect, url_for, flash
from flask_login import login_user, logout_user, UserMixin
from quokka.db import db
from quokka.template import render_template


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

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.users.find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
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

    app.add_quokka_url_rule(
        '/login/', view_func=login, methods=['GET', 'POST'], endpoint='login'
    )

    app.add_quokka_url_rule(
        '/logout/', view_func=logout, endpoint='logout'
    )
