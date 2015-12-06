#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from werkzeug import secure_filename
from flask import redirect, request, url_for, flash
from flask.views import MethodView
from quokka.utils import get_current_user
from quokka.utils.upload import lazy_media_path
from flask.ext.security.utils import url_for_security
from flask.ext.security import current_user
from flask.ext.mongoengine.wtf import model_form
from quokka.core.templates import render_template
from .models import User


class SwatchView(MethodView):
    """
    change the bootswatch theme
    """

    def post(self):
        swatch = request.form.get('swatch')
        current_user.set_swatch(swatch)
        flash('Theme successfully changed to %s' % swatch, 'alert')
        return redirect(url_for('admin.index'))


class ProfileView(MethodView):
    """
    Show User Profile
    """

    def get(self, user_id):
        return render_template('accounts/profile.html')


class ProfileEditView(MethodView):
    """
    Edit User Profile
    """

    form = model_form(
        User,
        only=[
            'name',
            'email',
            'username',
            'tagline',
            'bio',
            'use_avatar_from',
            'avatar_file_path',
            'gravatar_email',
            'avatar_url',
            'links',
        ]
    )

    @staticmethod
    def needs_login(**kwargs):
        if not current_user.is_authenticated():
            nex = kwargs.get(
                'next',
                request.values.get(
                    'next',
                    url_for('quokka.modules.accounts.profile_edit')
                )
            )
            return redirect(url_for_security('login', next=nex))

    def get(self):
        return self.needs_login() or render_template(
            'accounts/profile_edit.html',
            form=self.form(instance=get_current_user())
        )

    def post(self):
        form = self.form(request.form)
        if form.validate():
            user = get_current_user()
            avatar_file_path = user.avatar_file_path
            avatar = request.files.get('avatar')
            if avatar:
                filename = secure_filename(avatar.filename)
                avatar_file_path = os.path.join(
                    'avatars', str(user.id), filename
                )
                path = os.path.join(lazy_media_path(), avatar_file_path)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path), 0o777)
                avatar.save(path)
            form.populate_obj(user)
            user.avatar_file_path = avatar_file_path
            user.save()
            flash('Profile saved!', 'alert')
            return redirect(url_for('quokka.modules.accounts.profile_edit'))
        else:
            flash('Error ocurred!', 'alert error')  # form errors
            return render_template('accounts/profile_edit.html', form=form)
