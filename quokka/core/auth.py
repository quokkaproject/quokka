import getpass
from flask import current_app, url_for, Markup
from flask_htmlbuilder.htmlbuilder import html
from quokka.admin.actions import UserProfileBlockAction
from quokka.admin.views import ModelView
from quokka.admin.forms import Form, fields, ValidationError, validators
from quokka.utils.text import slugify
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
        [validators.required()],
        description='used as login'
    )
    fullname = fields.StringField(
        'Full Name',
        [validators.required()],
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


def format_profile(self, request, obj, fieldname, *args, **kwargs):
    """IF user has a profile page return a link to it"""
    existing_profile = current_app.db.index.find_one(
        {'content_type': 'block', 'slug': slugify(obj.get('fullname'))}
    )
    if existing_profile:
        edit_url = url_for(
            'quokka.core.content.admin.blockview.edit_view',
            id=existing_profile['_id']
        )
        view_url = url_for(
            'quokka.core.content.author',
            author=existing_profile['slug']
        )
        edit_link = html.a(href=edit_url, target='_blank')(
            html.i(class_="icon fa fa-pencil glyphicon glyphicon-pencil",
                   style="margin-right: 5px;")(),
            'Edit Profile'
        )
        view_link = html.a(href=view_url, target='_blank')(
            html.i(class_="icon fa fa-globe glyphicon glyphicon-globe",
                   style="margin-right: 5px;")(),
            'View Profile'
        )
        return html.div()(
            html.span()(edit_link),
            Markup('&nbsp;'),
            html.span()(view_link)
        )


class UserView(UserProfileBlockAction, ModelView):
    column_list = ('username', 'fullname', 'email', 'profile')
    column_sortable_list = ('username', 'fullname', 'email')

    form = UserForm

    page_size = 20
    can_set_page_size = True

    column_formatters = {
        'profile': format_profile
    }

    def on_form_prefill(self, form, id):
        # username cannot be changed
        form.username.render_kw = {'readonly': True}

    # Correct user_id reference before saving
    def on_model_change(self, form, model, is_created):
        username = model.get('username')
        password = model.get('password')

        if not model.get('fullname'):
            model['fullname'] = username

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

            # TODO: Update profile block if fullname changes?
            # TODO: Update all content author name if fullname changes?

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
