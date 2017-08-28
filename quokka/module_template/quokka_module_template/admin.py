from flask import current_app
from flask_admin.contrib.pymongo import filters
from flask_admin.form import Select2Widget
from flask_admin.model.fields import InlineFieldList, InlineFormField
from quokka.admin.forms import Form, fields
from quokka.admin.views import ModelView


# User admin
class InnerForm(Form):
    username = fields.StringField('Username')
    test = fields.StringField('Test')


class UserForm(Form):
    username = fields.StringField('Username')
    email = fields.StringField('Email')
    password = fields.StringField('Password')

    # Inner form
    inner = InlineFormField(InnerForm)

    # Form list
    form_list = InlineFieldList(InlineFormField(InnerForm))


class UserView(ModelView):
    column_list = ('username', 'email', 'password')
    column_sortable_list = ('username', 'email', 'password')

    form = UserForm

    page_size = 20
    can_set_page_size = True

    # Correct user_id reference before saving
    def on_model_change(self, form, model):
        model['_id'] = model.get('username')
        return model


# Tweet view
class TweetForm(Form):
    name = fields.StringField('Name')
    user_id = fields.SelectField('User', widget=Select2Widget())
    text = fields.StringField('Text')
    testie = fields.BooleanField('Test')


class TweetView(ModelView):
    column_list = ('name', 'user_name', 'text')
    column_sortable_list = ('name', 'text')

    column_filters = (filters.FilterEqual('name', 'Name'),
                      filters.FilterNotEqual('name', 'Name'),
                      filters.FilterLike('name', 'Name'),
                      filters.FilterNotLike('name', 'Name'),
                      filters.BooleanEqualFilter('testie', 'Testie'))

    # column_searchable_list = ('name', 'text')

    form = TweetForm

    def get_list(self, *args, **kwargs):
        # not necessary but kept as example
        count, data = super(TweetView, self).get_list(*args, **kwargs)

        # Contribute user_name to the models
        for item in data:
            user = current_app.db.users.find_one(
                {'_id': item['user_id']}
            )
            if user:
                item['user_name'] = user['_id']

        return count, data

    # Contribute list of user choices to the forms
    def _feed_user_choices(self, form):
        users = current_app.db.users.find(fields=('_id',))
        form.user_id.choices = [(str(x['_id']), x['_id']) for x in users]
        return form

    def create_form(self):
        form = super(TweetView, self).create_form()
        return self._feed_user_choices(form)

    def edit_form(self, obj):
        form = super(TweetView, self).edit_form(obj)
        return self._feed_user_choices(form)
