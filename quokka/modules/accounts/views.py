#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect, request, url_for
from flask.views import MethodView
from flask.ext.security import current_user


class SwatchView(MethodView):
    """
    change the bootswatch theme
    """

    def post(self):
        current_user.set_swatch(request.form.get('swatch'))
        return redirect(url_for('admin.index'))
