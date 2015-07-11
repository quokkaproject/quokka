# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
from flask import url_for

logger = logging.getLogger()

try:
    from flask_weasyprint import render_pdf

    import_error = False
except (ImportError, OSError) as e:

    # print("""
    # Error importing flask-weasyprint!
    # PDF support is temporarily disabled.
    # Manual dependencies may need to be installed.
    # See,
    #     `http://weasyprint.org/docs/install/#by-platform`_
    #     `https://github.com/Kozea/WeasyPrint/issues/79`_

    # """ + str(e))

    import_error = True


def configure(app):
    # only configure .pdf extension if it's enabled
    # and configured correctly in the environment.
    if app.config.get('ENABLE_TO_PDF', False) and not import_error:

        def render_to_pdf(long_slug):
            return render_pdf(url_for('detail', long_slug=long_slug))

        app.add_url_rule('/<path:long_slug>.pdf', view_func=render_to_pdf)
