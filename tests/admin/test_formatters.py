import pytest
import mock
from flask import current_app as app
from flask_htmlbuilder.htmlbuilder import html
from quokka.core.content.models import make_model
from quokka.admin.formatters import format_datetime, format_view_on_site, format_ul, \
                                    format_link, format_status, format_url, format_custom_vars
                                
